<template>
    <div class="agent-response">
        <div v-if="entries.length > 0" class="conversation-entries">
            <div
                v-for="(entry, index) in entries"
                :key="index"
                class="message-bubble"
                :class="entry.role === 'user' ? 'user-message' : 'agent-message'"
            >
                <div class="message-wrapper">
                    <div v-if="entry.role === 'assistant'" class="message-info">
                        <span class="text-caption text-medium-emphasis">
                            {{ entry.role === 'user' ? 'Vous' : agentName }}
                        </span>
                    </div>

                    <div class="message-content">
                        <div
                            :class="{
                                'text-body-1': true,
                                'text-white': entry.role === 'user',
                                'mb-0': true,
                                'ai-markdown-content': entry.role !== 'user',
                            }"
                            v-html="renderMarkdown(entry.content)"
                            @click="handleInlineLinks"
                        />

                        <div
                            v-if="entry.action_context"
                            :class="{
                                'text-body-1': true,
                                'text-white': entry.role === 'user',
                                'mb-0': true,
                                'ai-markdown-content': entry.role !== 'user',
                            }"
                        >
                            {{ JSON.stringify(entry.action_context) }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="agent-input-container mb-4">
            <div
                v-if="loadingState.loading"
                class="text-caption text-medium-emphasis mb-2 position-absolute mt-n6"
            >
                <v-progress-circular
                    indeterminate
                    size="14"
                    width="2"
                    color="primary"
                    class="me-2"
                />
                <span>{{loadingState.content || `${agentName} est en train de penser...`}}</span>
            </div>

            <v-text-field
                v-model="userMessage"
                :placeholder="`Posez votre question à ${agentName}...`"
                variant="outlined"
                class="agent-input rounded mt-12"
                autocomplete="off"
                @keyup.enter="onSendMessage"
            >
                <template #append-inner>
                    <v-btn
                        :disabled="!userMessage.trim() || loading"
                        :loading="loading"
                        color="primary"
                        variant="flat"
                        icon
                        size="small"
                        width="32"
                        height="32"
                        min-width="32"
                        min-height="32"
                        @click="onSendMessage"
                    >
                        <ArrowUp :size="16"/>
                    </v-btn>
                </template>
            </v-text-field>
        </div>
    </div>
</template>

<script setup>
import { useAgent } from '@/common/composables/agent';
import {
    ArrowUp,
} from 'lucide-vue-next';


const props = defineProps({
    agentName: {
        type: String,
        default: 'Trottr',
    },
});

const emit = defineEmits([
    'message-sent',
]);

const {
    loading,
    loadingState,
    userMessage,
    entries,
    sendMessage,
    renderMarkdown,
    handleInlineLinks,
} = useAgent();

const onSendMessage = async () => {
    if (userMessage.value?.trim()) {
        emit('message-sent', {message: userMessage});
        await sendMessage();
    }
};

const stripHtml = (html) => {
    if (!html) {
        return '';
    }

    return html.replace(/<[^>]*>/g, ' ').replace(/\s{2,}/g, ' ').trim();
};

/**
 * Sets the user message and optionally sends it immediately
 * @param {string} message - The message to set
 * @param {string|null} displayMessage - Optional display message override
 * @param {boolean} immediate - Whether to send the message immediately
 */
const setUserMessage = async (message, displayMessage = null, immediate = false) => {
    message = message?.trim() || '';

    if (message && message.includes('<')) {
        message = stripHtml(message);
    }

    userMessage.value = message;

    if (immediate) {
        await onSendMessage(displayMessage);
    }
};

defineExpose({
    setUserMessage,
    userMessage,
    entries,
    loadingState,
    loading,
});
</script>
