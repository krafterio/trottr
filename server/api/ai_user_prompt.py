from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Dict, Any, Optional, Union
from models.ai_user_prompt import AIUserPrompt
from models.user import User
from api.auth import get_current_user
from schemas.ai_user_prompt import AIUserPromptBase, AIUserPromptUpdate, AIUserPromptRead

router = APIRouter()

@router.get("", response_model=Dict[str, Any])
async def list_ai_user_prompts(
    limit: int = Query(80, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    is_home_prompt: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user),
):
    query = AIUserPrompt.query.filter(AIUserPrompt.columns.user == current_user.id)
    if is_home_prompt is not None:
        query = query.filter(AIUserPrompt.columns.is_home_prompt == is_home_prompt)
    total = await query.count()
    items = await query.order_by("-id").limit(limit).offset(offset).all()
    return {"total": total, "items": [item.dict() for item in items]}

@router.get("/{prompt_id}", response_model=AIUserPromptRead)
async def get_ai_user_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
):
    prompt = await AIUserPrompt.query.filter(
        (AIUserPrompt.columns.id == prompt_id) & (AIUserPrompt.columns.user == current_user.id)
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    return prompt.dict()

@router.post("", response_model=AIUserPromptRead)
async def create_ai_user_prompt(
    prompt: AIUserPromptBase,
    current_user: User = Depends(get_current_user),
):
    try:
        new_prompt = AIUserPrompt(
            name=prompt.name,
            emoji=prompt.emoji,
            content=prompt.content,
            user=current_user.id,
            is_home_prompt=prompt.is_home_prompt,
        )
        await new_prompt.save()
        return new_prompt.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création du prompt: {str(e)}")

@router.patch("/{prompt_id}", response_model=AIUserPromptRead)
async def update_ai_user_prompt(
    prompt_id: int,
    prompt_update: AIUserPromptUpdate,
    current_user: User = Depends(get_current_user),
):
    prompt = await AIUserPrompt.query.filter(
        (AIUserPrompt.columns.id == prompt_id) & (AIUserPrompt.columns.user == current_user.id)
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    update_data = prompt_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(prompt, field, value)
    try:
        await prompt.save()
        return prompt.dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour du prompt: {str(e)}")

@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_user_prompt(
    prompt_id: int,
    current_user: User = Depends(get_current_user),
):
    prompt = await AIUserPrompt.query.filter(
        (AIUserPrompt.columns.id == prompt_id) & (AIUserPrompt.columns.user == current_user.id)
    ).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt non trouvé")
    try:
        await prompt.delete()
        return None
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression du prompt: {str(e)}") 