import {ref} from 'vue';
import {useFetcher} from '@/common/composables/fetcher';
import {parseJsonLines} from '@/common/utils/stream';
import {marked} from 'marked';

/**
 * Composable to manage interactions with the AI agent.
 *
 * @returns {Object} Methods and states to interact with the AI agent
 */
export function useAgent() {
    const fetcher = useFetcher();

    const loading = ref(false);
    const loadingState = ref({
        loading: false,
        type: null,
        content: null,
    });
    const userMessage = ref('');
    const conversationId = ref(null);
    const entries = ref([]);

    /**
     * Sends a message to the AI agent and processes the streamed response.
     */
    const sendMessage = async () => {
        if (!userMessage.value || !userMessage.value.trim()) {
            return false;
        }

        let success = true;
        const userInput = {
            role: 'user',
            type: 'message.input',
            object: 'entry',
            content: userMessage.value,
        }

        loading.value = true;
        entries.value.push({
            role: 'user',
            content: userMessage.value,
        });
        userMessage.value = '';

        try {
            const response = await fetcher.post('/ai-agent/entries/stream', {
                conversation_id: conversationId.value,
                inputs: [userInput],
            });

            for await (const entry of parseJsonLines(response)) {
                if (entry.type === 'notification' && entry.content?.conversation_id) {
                    conversationId.value = entry.content?.conversation_id;
                } else if (entry.type === 'state') {
                    loadingState.value.loading = !!entry.content?.[0]?.loading;
                    loadingState.value.type = (loadingState.value.loading ? entry.content?.[0]?.type : null) || null;
                    loadingState.value.content = (loadingState.value.loading ? entry.content?.[0]?.content : null) || null;
                } else if (['message.input', 'message.output'].includes(entry.type)) {
                    if (typeof entry.content === 'object' && Array.isArray(entry.content)) {
                        const lastEntry = entries.value[entries.value.length - 1];

                        if (lastEntry && lastEntry.type === entry.type) {
                            entry.content.forEach((item) => {
                                if (item.type === 'text') {
                                    lastEntry.content += item.text;
                                }
                            });
                        } else {
                            let newEntryContent = '';
                            entry.content.forEach((item) => {
                                if (item.type === 'text') {
                                    newEntryContent += item.text;
                                }
                            });

                            entries.value.push({
                                ...entry,
                                role: entry.type === 'message.output' ? 'assistant' : entry.type,
                                content: newEntryContent,
                            });
                        }

                        continue;
                    }

                    entries.value.push({
                        ...entry,
                        role: entry.type === 'message.output' ? 'assistant' : entry.type,
                    });
                }
            }
        } catch (error) {
            success = false;
            console.error('Error sending message:', error);
        } finally {
            loading.value = false;
        }

        return success;
    }

    /**
     * Converts Markdown text to HTML.
     *
     * @param {string} content - Content in Markdown format
     * @returns {string} Content in HTML format
     */
    const renderMarkdown = (content) => {
        if (!content) {
            return '';
        }

        try {
            return marked.parse(content, {
                breaks: true,
                gfm: true,
            });
        } catch (error) {
            return content;
        }
    }

    /**
     * Handles clicks on links in Markdown content.
     *
     * @param {Event} event - The click event
     */
    const handleInlineLinks = (event) => {
        if (event.target.tagName === 'A') {
            event.preventDefault();
            const href = event.target.getAttribute('href');

            if (href) {
                const url = (href.startsWith('/') ? window.location.origin : '') + href;
                window.open(url, '_blank');
            }
        }
    }

    return {
        loading,
        loadingState,
        userMessage,
        conversationId,
        entries,
        sendMessage,
        renderMarkdown,
        handleInlineLinks,
    };
}
