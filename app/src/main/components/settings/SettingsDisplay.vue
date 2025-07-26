<template>
    <div class="max-w-2xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Affichage</h2>
            <p class="text-neutral-600">Personnalisez l'apparence de l'interface.</p>
        </div>

        <div class="space-y-6">
            <div class="space-y-2">
                <Label for="theme">Thème</Label>
                <Select>
                    <SelectTrigger class="max-w-sm">
                        <SelectValue placeholder="Sélectionner un thème" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="light">Clair</SelectItem>
                        <SelectItem value="dark">Sombre</SelectItem>
                        <SelectItem value="system">Système</SelectItem>
                    </SelectContent>
                </Select>
            </div>

            <div class="space-y-2">
                <Label for="language">Langue</Label>
                <Select>
                    <SelectTrigger class="max-w-sm">
                        <SelectValue placeholder="Sélectionner une langue" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="fr">Français</SelectItem>
                        <SelectItem value="en">English</SelectItem>
                        <SelectItem value="es">Español</SelectItem>
                    </SelectContent>
                </Select>
            </div>

            <div class="space-y-2">
                <Label for="density">Densité d'affichage</Label>
                <Select>
                    <SelectTrigger class="max-w-sm">
                        <SelectValue placeholder="Sélectionner une densité" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="compact">Compacte</SelectItem>
                        <SelectItem value="normal">Normale</SelectItem>
                        <SelectItem value="comfortable">Confortable</SelectItem>
                    </SelectContent>
                </Select>
            </div>

            <Separator />

            <div class="flex justify-end">
                <Button>
                    Appliquer les modifications
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Label } from '@/common/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
</script>