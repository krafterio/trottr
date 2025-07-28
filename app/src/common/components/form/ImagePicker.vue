<template>
  <!-- Mode Avatar minimaliste -->
  <div v-if="avatar" class="relative group w-16">
    <Avatar :class="[avatarClass, 'h-16', 'w-16', 'cursor-pointer', 'rounded-md']" @click="triggerFileInput">
      <AvatarImage v-if="modelValue && !imageError" :src="imageUrl" :alt="alt" v-fetcher-src.lazy />
      <AvatarFallback :class="[avatarClass, 'bg-muted']">
        <slot name="placeholder">
          <Image class="w-6 h-6 text-muted-foreground" />
        </slot>
      </AvatarFallback>
    </Avatar>

    <!-- Bouton supprimer en overlay quand image existe -->
    <Button v-if="modelValue && !uploading" type="button" variant="destructive" size="sm"
      class="absolute -bottom-1 -right-1 h-6 w-6 p-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
      @click.stop="removeImage">
      <Trash2 class="h-3 w-3" />
    </Button>

    <!-- Indicateur de chargement -->
    <div v-if="uploading" class="absolute inset-0 bg-black/50 rounded-full flex items-center justify-center">
      <Loader2 class="h-4 w-4 text-white animate-spin" />
    </div>

    <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange" />
  </div>

  <!-- Mode classique -->
  <div v-else class="flex items-start gap-4">
    <!-- Avatar à gauche -->
    <div class="flex-shrink-0">
      <Avatar class="w-16 h-16 cursor-pointer" @click="triggerFileInput">
        <AvatarImage v-if="modelValue && !imageError" :src="imageUrl" :alt="alt" v-fetcher-src.lazy />
        <AvatarFallback class="bg-muted">
          <Upload class="w-6 h-6 text-muted-foreground" />
        </AvatarFallback>
      </Avatar>
      <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileChange" />
    </div>

    <!-- Contenu à droite -->
    <div class="flex-1 space-y-3">
      <div class="flex items-center gap-2">
        <!-- Bouton Téléverser -->
        <Button type="button" variant="outline" size="sm" @click="triggerFileInput" :disabled="uploading">
          <Upload v-if="!uploading" class="h-4 w-4 mr-2" />
          <Loader2 v-else class="h-4 w-4 mr-2 animate-spin" />
          {{ modelValue ? 'Modifier' : 'Téléverser' }}
        </Button>

        <!-- Bouton Retirer (si image existe) -->
        <Button v-if="modelValue" type="button" variant="outline" size="sm" @click="removeImage" :disabled="uploading">
          <Trash2 class="h-4 w-4 mr-2" />
          Retirer
        </Button>
      </div>

      <!-- Message d'information -->
      <p v-if="helpText" class="text-sm text-muted-foreground">
        {{ helpText }}
      </p>

      <!-- Message d'erreur -->
      <div v-if="error" class="text-sm text-destructive">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Button } from '@/common/components/ui/button'
import { Image, Loader2, Trash2, Upload } from 'lucide-vue-next'
import { computed, ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: null
  },
  alt: {
    type: String,
    default: 'Image'
  },
  helpText: {
    type: String,
    default: null
  },
  maxSize: {
    type: Number,
    default: 5 * 1024 * 1024 // 5MB par défaut
  },
  acceptedFormats: {
    type: Array,
    default: () => ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
  },
  avatar: {
    type: Boolean,
    default: false
  },
  avatarClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'upload', 'remove', 'error'])

const fileInput = ref(null)
const uploading = ref(false)
const imageError = ref(false)
const error = ref('')

const imageUrl = computed(() => {
  if (!props.modelValue) return null

  if (props.modelValue.startsWith('http') || props.modelValue.startsWith('data:')) {
    return props.modelValue
  }

  return `/storage/download/${props.modelValue}`
})

const triggerFileInput = () => {
  if (!uploading.value) {
    fileInput.value?.click()
  }
}

const handleFileChange = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  error.value = ''

  // Validation du type de fichier
  if (!props.acceptedFormats.includes(file.type)) {
    error.value = 'Format de fichier non supporté'
    emit('error', error.value)
    return
  }

  // Validation de la taille
  if (file.size > props.maxSize) {
    error.value = `Le fichier est trop volumineux (max ${Math.round(props.maxSize / 1024 / 1024)}MB)`
    emit('error', error.value)
    return
  }

  uploading.value = true

  try {
    emit('upload', file)
  } catch (err) {
    error.value = 'Erreur lors du téléversement'
    emit('error', error.value)
  } finally {
    uploading.value = false

    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

const removeImage = () => {
  if (!uploading.value) {
    emit('remove')
    emit('update:modelValue', null)
    imageError.value = false
    error.value = ''
  }
}

// Gérer les erreurs de chargement d'image
const handleImageError = () => {
  imageError.value = true
}

</script>
