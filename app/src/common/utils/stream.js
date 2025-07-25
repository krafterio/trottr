
/**
 * Parse a JSON Lines from the fetch response
 *
 * @param {Response} response - The fetch response with a JSON Lines body
 * @returns {AsyncGenerator<Object>}
 */
export async function* parseJsonLines(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');

    let buffer = '';
    let error = null;

    try {
        while (true) {
            const {value, done} = await reader.read();

            if (done) {
                break;
            }

            buffer += decoder.decode(value, {stream: true});
            const lines = buffer.split("\n");
            buffer = lines.pop();

            for (const line of lines) {
                if (line.trim()) {
                    yield JSON.parse(line);
                }
            }
        }

        if (buffer.trim()) {
            yield JSON.parse(buffer);
        }
    } catch (err) {
        if (err.name !== "AbortError") {
            error = err;
        }
    } finally {
        reader.releaseLock();
    }

    if (error) {
        throw error;
    }
}
