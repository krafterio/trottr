# RelationSelect

Composant générique **scalable** pour les relations many-to-one avec recherche en temps réel.

## 🚀 Utilisation de base

```vue
<RelationSelect 
    v-model="selectedCompany"
    endpoint="/companies"
    display-field="name"
    image-field="logo"
    placeholder="Sélectionner une société..."
    :clearable="true"
/>
```

## 📋 Props principales

| Prop | Type | Défaut | Description |
|------|------|--------|-------------|
| `endpoint` | String | **required** | URL de l'API (ex: `/companies`) |
| `display-field` | String | `'name'` | Champ à afficher comme texte |
| `image-field` | String | `null` | Champ image (optionnel) |
| `subtitle-field` | String | `null` | Champ sous-titre (optionnel) |
| `extra-fields` | Array | `[]` | Champs supplémentaires à récupérer |
| `clearable` | Boolean | `false` | Bouton pour vider la sélection |

## 🎨 Slots customisables

### `selected-item` - Item sélectionné dans le trigger

```vue
<RelationSelect v-model="company" endpoint="/companies">
    <template #selected-item="{ item }">
        <Avatar class="h-4 w-4">
            <AvatarImage :src="item.logo" />
        </Avatar>
        <span class="font-bold">{{ item.name }}</span>
        <Badge>{{ item.domain }}</Badge>
    </template>
</RelationSelect>
```

### `list-item` - Items dans le dropdown

```vue
<RelationSelect v-model="company" endpoint="/companies">
    <template #list-item="{ item }">
        <div class="custom-layout">
            <img :src="item.logo" class="w-8 h-8" />
            <div>
                <div class="font-semibold">{{ item.name }}</div>
                <div class="text-sm text-gray-500">{{ item.industry }}</div>
            </div>
        </div>
    </template>
</RelationSelect>
```

## 📊 Exemples avancés

### Avec champs supplémentaires
```vue
<RelationSelect 
    v-model="contact"
    endpoint="/contacts"
    display-field="full_name"
    image-field="photo_url"
    subtitle-field="email"
    :extra-fields="['company_name', 'phone']"
/>
```

### Paramètres de recherche personnalisés
```vue
<RelationSelect 
    v-model="user"
    endpoint="/users"
    search-param="q"
    :min-search-length="3"
    :limit="100"
    :default-limit="20"
/>
```
