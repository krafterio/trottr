<template>
  <div class="online-users-container">
    <Popover v-model:open="showPopover">
      <PopoverTrigger as-child>
        <Button variant="ghost" size="sm" class="hidden lg:flex items-center px-2 h-10">
          <div class="flex items-center -space-x-2" ref="avatarsContainer">
            <template v-for="(user, index) in visibleUsers" :key="user.id">
              <div 
                class="relative inline-block transition-transform duration-200 hover:z-10 hover:scale-110"
                :style="{ zIndex: visibleUsers.length - index }"
                @mouseenter="(e) => showTooltipFor(e, user)"
                @mouseleave="hideTooltip"
              >
                <Avatar class="w-6 h-6 border-2 border-background ring-1 ring-border">
                  <AvatarImage v-if="user.avatar" :src="getAvatarUrl(user)" v-fetcher-src.lazy :alt="user.name || user.email" />
                  <AvatarFallback class="text-xs bg-primary text-primary-foreground">
                    {{ user.initials }}
                  </AvatarFallback>
                </Avatar>
              </div>
            </template>
            
            <div 
              v-if="moreUsers > 0"
              class="relative inline-block transition-transform duration-200 hover:z-10 hover:scale-110"
              @mouseenter="(e) => showTooltipFor(e, { name: 'Plus d\'utilisateurs en ligne' })"
              @mouseleave="hideTooltip"
            >
              <Avatar class="w-6 h-6 border-2 border-background ring-1 ring-border">
                <AvatarFallback class="text-xs bg-muted text-muted-foreground">
                  +{{ moreUsers }}
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </Button>
      </PopoverTrigger>
      
      <PopoverContent class="w-60 p-0 overflow-hidden" align="end" :side-offset="5">
        <div class="p-3 pb-2">
          <h4 class="text-sm font-medium">
            Utilisateurs en ligne ({{ onlineUsers.length }})
          </h4>
        </div>

        <Separator />

        <div class="max-h-48 overflow-y-auto">
          <div 
            v-for="user in onlineUsers"
            :key="user.id"
            class="flex items-center gap-3 p-3 hover:bg-accent transition-colors"
          >
            <Avatar class="w-8 h-8">
              <AvatarImage v-if="user.avatar" :src="getAvatarUrl(user)" v-fetcher-src.lazy :alt="user.name || user.email" />
              <AvatarFallback class="text-xs bg-primary text-primary-foreground">
                {{ user.initials }}
              </AvatarFallback>
            </Avatar>
        
            <span class="text-sm truncate">{{ user.name || user.email }}</span>
          </div>
        </div>
      </PopoverContent>
    </Popover>

    <div
      v-if="tooltipVisible"
      class="fixed z-50 px-2 py-1 text-xs bg-popover text-popover-foreground border rounded-md shadow-lg pointer-events-none"
      :style="tooltipStyle"
    >
      {{ tooltipText }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { usePresenceStore } from "@/common/stores/presence"
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Button } from '@/common/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/common/components/ui/popover'
import { Separator } from '@/common/components/ui/separator'

const props = defineProps({
  maxUsers: {
    type: Number,
    default: 3,
  }
})

const presenceStore = usePresenceStore()
const showPopover = ref(false)
const avatarsContainer = ref(null)

const tooltipVisible = ref(false)
const tooltipText = ref('')
const tooltipTarget = ref(null)
const tooltipStyle = ref({})

const onlineUsers = computed(() => presenceStore.onlineUsers)

const visibleUsers = computed(() => {
  return onlineUsers.value.slice(0, props.maxUsers)
})

const moreUsers = computed(() => {
  return onlineUsers.value.length - visibleUsers.value.length
})

watch(showPopover, (newValue) => {
  if (newValue === true) {
    tooltipVisible.value = false
  }
})

const showTooltipFor = async (event, user) => {
  if (showPopover.value) {
    return
  }

  tooltipText.value = user.name || user.email
  tooltipTarget.value = event.currentTarget
  
  await nextTick()
  
  const rect = event.currentTarget.getBoundingClientRect()
  tooltipStyle.value = {
    top: `${rect.bottom + 8}px`,
    left: `${rect.left + rect.width / 2}px`,
    transform: 'translateX(-50%)'
  }
  
  tooltipVisible.value = true
}

const hideTooltip = () => {
  tooltipVisible.value = false
}

const getAvatarUrl = (user) => {
  return `/storage/download/${user.avatar}`
}
</script>

<style scoped>
.online-users-container {
  margin-left: 16px;
}
</style>
