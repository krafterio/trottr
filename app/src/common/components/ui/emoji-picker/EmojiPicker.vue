<template>
  <div 
    class="bg-popover text-popover-foreground isolate flex h-full w-80 flex-col overflow-hidden rounded-md border shadow-md"
    :class="className"
  >
    <!-- Search -->
    <div class="flex h-9 items-center gap-2 border-b px-3">
      <Search class="w-4 h-4 shrink-0 opacity-50" />
      <input
        v-model="searchQuery"
        class="outline-none placeholder:text-muted-foreground flex h-10 w-full rounded-md bg-transparent py-3 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        placeholder="Rechercher un emoji..."
      />
    </div>

    <!-- Content -->
    <div class="outline-none relative flex-1 max-h-64 overflow-y-auto">
      <div v-if="loading" class="absolute inset-0 flex items-center justify-center text-muted-foreground">
        <Loader class="w-4 h-4 animate-spin" />
      </div>
      
      <div v-else-if="filteredEmojis.length === 0" class="absolute inset-0 flex items-center justify-center text-muted-foreground text-sm">
        Aucun emoji trouvé.
      </div>
      
      <div v-else class="select-none pb-1">
        <div v-for="category in filteredCategories" :key="category.name" class="scroll-my-1 px-1">
          <div class="bg-popover text-muted-foreground px-3 pb-2 pt-3.5 text-xs leading-none">
            {{ category.label }}
          </div>
          <div class="grid grid-cols-8 gap-1 px-2 pb-2">
            <button
              v-for="emoji in category.emojis"
              :key="emoji.emoji"
              type="button"
              @click="selectEmoji(emoji)"
              @mouseenter="setActiveEmoji(emoji)"
              @mouseleave="setActiveEmoji(null)"
              class="flex w-7 h-7 items-center justify-center rounded-sm text-base hover:bg-accent transition-colors"
              :class="{ 'bg-accent': activeEmoji?.emoji === emoji.emoji }"
            >
              {{ emoji.emoji }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="flex w-full min-w-0 items-center gap-1 border-t p-2">
      <div v-if="activeEmoji" class="flex items-center gap-2">
        <div class="flex w-7 h-7 flex-none items-center justify-center text-lg">
          {{ activeEmoji.emoji }}
        </div>
        <span class="text-secondary-foreground truncate text-xs">
          {{ activeEmoji.label }}
        </span>
      </div>
      <span v-else class="text-muted-foreground ml-1.5 flex h-7 items-center truncate text-xs">
        Sélectionnez un emoji…
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, Loader } from 'lucide-vue-next'

const props = defineProps({
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['select'])

const searchQuery = ref('')
const activeEmoji = ref(null)
const loading = ref(true)
const allEmojis = ref([])

// Quelques emojis de base pour commencer
const basicEmojis = [
  { emoji: '😀', label: 'Visage souriant' },
  { emoji: '😃', label: 'Visage souriant avec de gros yeux' },
  { emoji: '😄', label: 'Visage souriant avec les yeux qui sourient' },
  { emoji: '😁', label: 'Visage rayonnant avec les yeux qui sourient' },
  { emoji: '😆', label: 'Visage souriant avec les yeux fermés' },
  { emoji: '😅', label: 'Visage souriant avec une goutte de sueur' },
  { emoji: '🤣', label: 'Visage qui pleure de rire' },
  { emoji: '😂', label: 'Visage avec des larmes de joie' },
  { emoji: '🙂', label: 'Visage légèrement souriant' },
  { emoji: '🙃', label: 'Visage à l\'envers' },
  { emoji: '😉', label: 'Visage qui fait un clin d\'œil' },
  { emoji: '😊', label: 'Visage souriant avec les yeux qui sourient' },
  { emoji: '😇', label: 'Visage souriant avec une auréole' },
  { emoji: '🥰', label: 'Visage souriant avec des cœurs' },
  { emoji: '😍', label: 'Visage souriant avec des yeux en forme de cœur' },
  { emoji: '🤩', label: 'Visage étoilé' },
  { emoji: '😘', label: 'Visage envoyant un bisou' },
  { emoji: '😗', label: 'Visage qui fait un bisou' },
  { emoji: '☺️', label: 'Visage souriant' },
  { emoji: '😚', label: 'Visage qui fait un bisou avec les yeux fermés' },
  { emoji: '😙', label: 'Visage qui fait un bisou avec les yeux qui sourient' },
  { emoji: '🥲', label: 'Visage souriant avec une larme' },
  { emoji: '😋', label: 'Visage savourant la nourriture' },
  { emoji: '😛', label: 'Visage avec la langue qui sort' },
  { emoji: '😜', label: 'Visage qui fait un clin d\'œil avec la langue qui sort' },
  { emoji: '🤪', label: 'Visage fou' },
  { emoji: '😝', label: 'Visage avec la langue qui sort et les yeux fermés' },
  { emoji: '🤑', label: 'Visage avec la bouche d\'argent' },
  { emoji: '🤗', label: 'Visage qui fait un câlin' },
  { emoji: '🤭', label: 'Visage avec la main sur la bouche' },
  { emoji: '🤫', label: 'Visage faisant chut' },
  { emoji: '🤔', label: 'Visage pensif' },
  { emoji: '🤐', label: 'Visage avec la bouche fermée par une fermeture éclair' },
  { emoji: '🤨', label: 'Visage avec un sourcil levé' },
  { emoji: '😐', label: 'Visage neutre' },
  { emoji: '😑', label: 'Visage sans expression' },
  { emoji: '😶', label: 'Visage sans bouche' },
  { emoji: '😏', label: 'Visage narquois' },
  { emoji: '😒', label: 'Visage blasé' },
  { emoji: '🙄', label: 'Visage avec les yeux qui roulent' },
  { emoji: '😬', label: 'Visage grimaçant' },
  { emoji: '🤥', label: 'Visage menteur' },
  { emoji: '😔', label: 'Visage pensif' },
  { emoji: '😪', label: 'Visage endormi' },
  { emoji: '🤤', label: 'Visage qui bave' },
  { emoji: '😴', label: 'Visage endormi' },
  { emoji: '😷', label: 'Visage avec un masque médical' },
  { emoji: '🤒', label: 'Visage avec un thermomètre' },
  { emoji: '🤕', label: 'Visage avec un bandage sur la tête' },
  { emoji: '🤢', label: 'Visage nauséeux' },
  { emoji: '🤮', label: 'Visage qui vomit' },
  { emoji: '🤧', label: 'Visage qui éternue' },
  { emoji: '🥵', label: 'Visage surchauffé' },
  { emoji: '🥶', label: 'Visage gelé' },
  { emoji: '🥴', label: 'Visage étourdi' },
  { emoji: '😵', label: 'Visage étourdi' },
  { emoji: '🤯', label: 'Tête qui explose' },
  { emoji: '🤠', label: 'Visage de cow-boy' },
  { emoji: '🥳', label: 'Visage de fête' },
  { emoji: '🥸', label: 'Visage déguisé' },
  { emoji: '😎', label: 'Visage souriant avec des lunettes de soleil' },
  { emoji: '🤓', label: 'Visage de nerd' },
  { emoji: '🧐', label: 'Visage avec un monocle' },
  { emoji: '😕', label: 'Visage confus' },
  { emoji: '😟', label: 'Visage inquiet' },
  { emoji: '🙁', label: 'Visage légèrement froncé' },
  { emoji: '☹️', label: 'Visage qui fronce les sourcils' },
  { emoji: '😮', label: 'Visage avec la bouche ouverte' },
  { emoji: '😯', label: 'Visage stupéfait' },
  { emoji: '😲', label: 'Visage étonné' },
  { emoji: '😳', label: 'Visage qui rougit' },
  { emoji: '🥺', label: 'Visage suppliant' },
  { emoji: '😦', label: 'Visage froncé avec la bouche ouverte' },
  { emoji: '😧', label: 'Visage angoissé' },
  { emoji: '😨', label: 'Visage effrayé' },
  { emoji: '😰', label: 'Visage anxieux avec de la sueur' },
  { emoji: '😥', label: 'Visage triste mais soulagé' },
  { emoji: '😢', label: 'Visage qui pleure' },
  { emoji: '😭', label: 'Visage qui pleure très fort' },
  { emoji: '😱', label: 'Visage qui crie de peur' },
  { emoji: '😖', label: 'Visage confus' },
  { emoji: '😣', label: 'Visage qui persévère' },
  { emoji: '😞', label: 'Visage déçu' },
  { emoji: '😓', label: 'Visage qui transpire' },
  { emoji: '😩', label: 'Visage las' },
  { emoji: '😫', label: 'Visage fatigué' },
  { emoji: '🥱', label: 'Visage qui bâille' },
  { emoji: '😤', label: 'Visage avec de la vapeur par le nez' },
  { emoji: '😡', label: 'Visage rouge de colère' },
  { emoji: '😠', label: 'Visage en colère' },
  { emoji: '🤬', label: 'Visage avec des symboles sur la bouche' },
  { emoji: '😈', label: 'Visage souriant avec des cornes' },
  { emoji: '👿', label: 'Visage en colère avec des cornes' },
  { emoji: '💀', label: 'Crâne' },
  { emoji: '☠️', label: 'Crâne et os croisés' },
  { emoji: '💩', label: 'Tas de crottes' },
  { emoji: '🤡', label: 'Visage de clown' },
  { emoji: '👹', label: 'Ogre' },
  { emoji: '👺', label: 'Goblin' },
  { emoji: '👻', label: 'Fantôme' },
  { emoji: '👽', label: 'Extraterrestre' },
  { emoji: '👾', label: 'Monstre extraterrestre' },
  { emoji: '🤖', label: 'Robot' },
  { emoji: '😺', label: 'Chat souriant' },
  { emoji: '😸', label: 'Chat souriant avec les yeux qui sourient' },
  { emoji: '😹', label: 'Chat avec des larmes de joie' },
  { emoji: '😻', label: 'Chat souriant avec des yeux en forme de cœur' },
  { emoji: '😼', label: 'Chat avec un sourire narquois' },
  { emoji: '😽', label: 'Chat qui fait un bisou' },
  { emoji: '🙀', label: 'Chat fatigué' },
  { emoji: '😿', label: 'Chat qui pleure' },
  { emoji: '😾', label: 'Chat boudeur' },
  { emoji: '❤️', label: 'Cœur rouge' },
  { emoji: '🧡', label: 'Cœur orange' },
  { emoji: '💛', label: 'Cœur jaune' },
  { emoji: '💚', label: 'Cœur vert' },
  { emoji: '💙', label: 'Cœur bleu' },
  { emoji: '💜', label: 'Cœur violet' },
  { emoji: '🤎', label: 'Cœur marron' },
  { emoji: '🖤', label: 'Cœur noir' },
  { emoji: '🤍', label: 'Cœur blanc' },
  { emoji: '💔', label: 'Cœur brisé' },
  { emoji: '❣️', label: 'Cœur décoratif' },
  { emoji: '💕', label: 'Deux cœurs' },
  { emoji: '💞', label: 'Cœurs qui tournent' },
  { emoji: '💓', label: 'Cœur qui bat' },
  { emoji: '💗', label: 'Cœur qui grandit' },
  { emoji: '💖', label: 'Cœur brillant' },
  { emoji: '💘', label: 'Cœur avec une flèche' },
  { emoji: '💝', label: 'Cœur avec un ruban' },
  { emoji: '💟', label: 'Décoration de cœur' },
  { emoji: '♥️', label: 'Symbole de cœur' },
  { emoji: '💯', label: 'Symbole cent points' },
  { emoji: '💢', label: 'Symbole de colère' },
  { emoji: '💥', label: 'Symbole de collision' },
  { emoji: '💫', label: 'Symbole d\'étourdissement' },
  { emoji: '💦', label: 'Symbole d\'éclaboussure de sueur' },
  { emoji: '💨', label: 'Symbole de vitesse' },
  { emoji: '🕳️', label: 'Trou' },
  { emoji: '💣', label: 'Bombe' },
  { emoji: '💬', label: 'Bulle de dialogue' },
  { emoji: '👁️‍🗨️', label: 'Œil dans une bulle de dialogue' },
  { emoji: '🗨️', label: 'Bulle de dialogue de gauche' },
  { emoji: '🗯️', label: 'Bulle de colère de droite' },
  { emoji: '💭', label: 'Bulle de pensée' },
  { emoji: '💤', label: 'Symbole de sommeil' }
]

const categories = [
  {
    name: 'smileys',
    label: 'Smileys & Émotion',
    emojis: basicEmojis.slice(0, 50)
  },
  {
    name: 'hearts',
    label: 'Cœurs',
    emojis: basicEmojis.slice(50, 70)
  },
  {
    name: 'symbols',
    label: 'Symboles',
    emojis: basicEmojis.slice(70)
  }
]

const filteredEmojis = computed(() => {
  if (!searchQuery.value) return basicEmojis
  
  return basicEmojis.filter(emoji => 
    emoji.label.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    emoji.emoji.includes(searchQuery.value)
  )
})

const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories
  
  return categories.map(category => ({
    ...category,
    emojis: category.emojis.filter(emoji => 
      emoji.label.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      emoji.emoji.includes(searchQuery.value)
    )
  })).filter(category => category.emojis.length > 0)
})

const setActiveEmoji = (emoji) => {
  activeEmoji.value = emoji
}

const selectEmoji = (emoji) => {
  emit('select', emoji.emoji)
}

onMounted(() => {
  // Simuler le chargement
  setTimeout(() => {
    allEmojis.value = basicEmojis
    loading.value = false
  }, 100)
})
</script> 