<template>
    <v-dialog :model-value="show" @update:model-value="updateShow" max-width="400">
        <v-card>
            <v-card-title>{{ title }}</v-card-title>
            <v-card-text>
                {{ message }}
                <strong v-if="itemName">"{{ itemName }}"</strong> ?
            </v-card-text>
            <v-card-actions class="justify-end">
                <v-btn @click="cancel" variant="text">Annuler</v-btn>
                <v-btn @click="confirm" :loading="loading" color="error">Supprimer</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
const props = defineProps({
    show: Boolean,
    title: String,
    message: String,
    itemName: String,
    loading: Boolean,
});

const emit = defineEmits([
    'update:show',
    'confirm',
    'cancel',
]);

const updateShow = (value) => {
    emit('update:show', value);
};

const confirm = () => {
    emit('confirm');
};

const cancel = () => {
    emit('cancel');
    emit('update:show', false);
};
</script> 
