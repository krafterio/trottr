<template>
    <div class="max-w-2xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Profil</h2>
            <p class="text-neutral-600">Voici comment les autres vous verront sur le site.</p>
        </div>

        <div class="space-y-6">
            <div class="space-y-2">
                <Label for="username">Nom d'utilisateur</Label>
                <Input id="username" v-model="username" placeholder="shadcn" class="max-w-sm" />
                <p class="text-sm text-neutral-500">
                    Ceci est votre nom d'affichage public. Il peut s'agir de votre vrai nom ou d'un pseudonyme.
                    Vous ne pouvez le modifier qu'une fois tous les 30 jours.
                </p>
            </div>

            <div class="space-y-2">
                <Label for="email">Email</Label>
                <Select>
                    <SelectTrigger class="max-w-sm">
                        <SelectValue placeholder="Sélectionner un email" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="email1">m@example.com</SelectItem>
                        <SelectItem value="email2">m@google.com</SelectItem>
                        <SelectItem value="email3">m@support.com</SelectItem>
                    </SelectContent>
                </Select>
                <p class="text-sm text-neutral-500">
                    Vous pouvez gérer les adresses email vérifiées dans vos paramètres d'email.
                </p>
            </div>

            <div class="space-y-2">
                <Label for="bio">Bio</Label>
                <Textarea id="bio" v-model="bio" placeholder="Je suis propriétaire d'un ordinateur." class="resize-none"
                    rows="3" />
                <p class="text-sm text-neutral-500">
                    Vous pouvez @mentionner d'autres utilisateurs et organisations pour créer un lien vers eux.
                </p>
            </div>

            <div class="space-y-4">
                <div class="space-y-2">
                    <Label>URLs</Label>
                    <p class="text-sm text-neutral-500">
                        Ajoutez des liens vers votre site web, blog ou profils de réseaux sociaux.
                    </p>
                </div>

                <div class="space-y-2">
                    <Input v-model="website" placeholder="https://exemple.com" class="max-w-sm" />
                    <Button variant="ghost" size="sm" class="text-neutral-600">
                        <Plus class="h-4 w-4 mr-2" />
                        Ajouter une URL
                    </Button>
                </div>
            </div>

            <Separator />

            <div class="flex justify-end">
                <Button @click="updateProfile">
                    Mettre à jour le profil
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Textarea } from '@/common/components/ui/textarea'
import { Plus } from 'lucide-vue-next'
import { ref } from 'vue'

const username = ref('shadcn')
const bio = ref('Je suis propriétaire d\'un ordinateur.')
const website = ref('')

const updateProfile = () => {
    console.log('Profil mis à jour')
}
</script>