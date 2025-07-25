<template>
    <div class="s-avatar-wrapper">        
        <div class="s-avatar-container" :class="{ 'has-image': hasImage }">
            <v-avatar
                :size="size"
                :color="hasImage ? undefined : 'grey-lighten-4'"
                class="s-avatar"
                @click="triggerFileInput"
                :loading="loading"
                :rounded="circle ? '' : undefined"
            >
                <SImg v-if="hasImage" :src="imageUrl" cover />
                <Image v-else :size="28" weight="regular" color="grey" />
            </v-avatar>
            
            <div v-if="hasImage" class="s-avatar-actions">
                <v-btn
                    size="x-small"
                    icon
                    variant="text"
                    color="error"
                    class="s-avatar-delete"
                    @click.stop="clearImage"
                >
                    <Trash :size="16" />
                </v-btn>
            </div>
            
            <input
                ref="fileInput"
                type="file"
                accept="image/*"
                class="s-avatar-input"
                @change="handleFileChange"
            />
        </div>        
    </div>
</template>

<script setup>
import { ref, computed, defineOptions } from 'vue';
import {
    Image,
    Trash,
} from 'lucide-vue-next';
import {useFetcher} from "@/common/composables/fetcher";
import SImg from "@/common/components/SImg.vue";

defineOptions({
    name: 's-avatar'
});

const props = defineProps({
    modelValue: {
        type: String,
        default: null
    },
    model: {
        type: String,
    },
    modelId: {
        type: [Number, String],
        default: null,
    },
    field: {
        type: String,
    },
    label: {
        type: String,
        default: ''
    },
    hint: {
        type: String,
        default: 'Cliquez pour ajouter une image'
    },
    size: {
        type: [Number, String],
        default: 80
    },
    circle: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['update:modelValue']);

const fetcher = useFetcher();

const fileInput = ref(null);
const loading = ref(false);
const hasImage = computed(() => !!props.modelValue);
const imageUrl = computed(() => {
    if (!props.modelValue) return null;
    
    // Si c'est une URL complète, retourner telle quelle
    if (props.modelValue.includes('//')) {
        return props.modelValue;
    }
    
    // Sinon, construire l'URL à partir du chemin relatif
    return `/storage/download/${props.modelValue}`;
});

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    loading.value = true;
    
    try {
        // Créer un FormData pour l'upload
        const formData = new FormData();
        formData.append('file', file);
        
        // Envoyer l'image au serveur
        const { data } = await fetcher.post(`/storage/upload/${props.model}/${props.modelId || 0}/${props.field}`, formData);
        
        // Émettre le chemin de l'image retourné par le serveur
        emit('update:modelValue', data);
    } catch (error) {
        console.error('Erreur lors de l\'upload d\'image:', error?.data, error);
        alert('Erreur lors de l\'upload de l\'image');
    } finally {
        loading.value = false;
    }
};

const clearImage = async () => {
    try {
        // Si une image est présente, la supprimer du serveur
        if (props.modelValue) {
            await fetcher.delete(`/storage/file/${props.model}/${props.modelId || 0}/${props.field}`);
        }
        
        // Réinitialiser la valeur
        emit('update:modelValue', null);
        if (fileInput.value) {
            fileInput.value.value = '';
        }
    } catch (error) {
        console.error('Erreur lors de la suppression de l\'image:', error);
        alert('Erreur lors de la suppression de l\'image');
    }
};
</script>