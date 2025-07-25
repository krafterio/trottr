from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import pandas as pd
import io
from typing import Dict, List, Any

from api.auth import get_current_user
from models.country import Country

router = APIRouter(tags=["import"])

ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls'}
ALLOWED_MIME_TYPES = {
    'text/csv',
    'application/vnd.ms-excel', 
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

@router.post("/upload")
async def upload_import_file(
    file: UploadFile = File(...),
    type: str = Form(...)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"Fichier trop volumineux. Taille maximale autorisée: {MAX_FILE_SIZE // (1024 * 1024)} MB"
        )
    
    file_extension = '.' + file.filename.split('.')[-1].lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail="Format de fichier non supporté. Utilisez CSV ou Excel (.xlsx, .xls)"
        )
    
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Type MIME non supporté"
        )
    
    try:
        contents = await file.read()
        
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"Fichier trop volumineux. Taille maximale autorisée: {MAX_FILE_SIZE // (1024 * 1024)} MB"
            )
        
        if file_extension == '.csv':
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Le fichier est vide")
        
        df = df.fillna('')
        
        headers = df.columns.tolist()
        sample_data = df.head(5).to_dict('records')
        rows_count = len(df)
        
        file_id = f"import_{type}_{hash(file.filename)}_{pd.Timestamp.now().timestamp()}"
        
        return JSONResponse({
            "file_id": file_id,
            "headers": headers,
            "sample_data": sample_data,
            "rows_count": rows_count,
            "filename": file.filename,
            "type": type
        })
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Le fichier est vide ou mal formaté")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Erreur lors de la lecture du fichier")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Encodage du fichier non supporté")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")


@router.post("/validate", dependencies=[Depends(get_current_user)])
async def validate_import(
    file: UploadFile = File(...),
    mapping: str = Form(...),
    type: str = Form(...),
    options: str = Form(default="{}")
):
    import json
    
    try:
        mapping_dict = json.loads(mapping)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Mapping JSON invalide")
    
    try:
        options_dict = json.loads(options)
    except json.JSONDecodeError:
        options_dict = {}
    
    # Extraire les options du mapping s'elles existent et nettoyer le mapping
    if '_options' in mapping_dict:
        mapping_options = mapping_dict.pop('_options')
        # Fusionner avec les options du paramètre séparé
        options_dict.update(mapping_options)
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")
    
    file_extension = '.' + file.filename.split('.')[-1].lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail="Format de fichier non supporté. Utilisez CSV ou Excel (.xlsx, .xls)"
        )
    
    try:
        contents = await file.read()
        
        if file_extension == '.csv':
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Le fichier est vide")
        
        df = df.fillna('')
        
        validation_errors = []
        valid_count = 0
        
        for index, row in df.iterrows():
            row_errors = {}
            
            for field_name, column_name in mapping_dict.items():
                if column_name and column_name in df.columns:
                    value = row[column_name]
                    if pd.isna(value) or value == '':
                        if field_name in ['first_name', 'last_name'] and type == 'contacts':
                            row_errors[field_name] = f"Le champ {field_name} est requis"
                        elif field_name == 'name' and type == 'companies':
                            row_errors[field_name] = f"Le champ {field_name} est requis"
            
            if type == 'contacts':
                has_first_name = mapping_dict.get('first_name') and mapping_dict['first_name'] in df.columns and pd.notna(row.get(mapping_dict['first_name'], '')) and row.get(mapping_dict['first_name'], '') != ''
                has_last_name = mapping_dict.get('last_name') and mapping_dict['last_name'] in df.columns and pd.notna(row.get(mapping_dict['last_name'], '')) and row.get(mapping_dict['last_name'], '') != ''
                
                if not has_first_name and not has_last_name:
                    if 'first_name' not in row_errors:
                        row_errors['first_name'] = "Au moins le prénom ou le nom est requis"
                    if 'last_name' not in row_errors:
                        row_errors['last_name'] = "Au moins le prénom ou le nom est requis"
            
            if row_errors:
                row_number = index + 2 if isinstance(index, int) else 2
                validation_errors.append({
                    'row': row_number,
                    'errors': row_errors
                })
            else:
                valid_count += 1
        
        return JSONResponse({
            "success": True,
            "valid_count": valid_count,
            "total_rows": len(df),
            "errors": validation_errors
        })
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Le fichier est vide ou mal formaté")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Erreur lors de la lecture du fichier")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Encodage du fichier non supporté")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la validation: {str(e)}")

