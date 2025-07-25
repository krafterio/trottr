import {EventBus} from '@/common/composables/bus';

export const fetchBus = new EventBus();

export class HttpError extends Error {
    /**
     * @param {Response} response
     * @param {String}   message
     * @param {Object}   [data]
     */
    constructor(response, message = undefined, data = undefined) {
        super(message);
        this.response = response;
        this.data = data;
    }
}

/**
 * [MDN Reference](https://developer.mozilla.org/docs/Web/API/fetch)
 *
 * @param {RequestInfo | URL}                                                url
 * @param {RequestInit | {params?: Object, body?: Object | BodyInit | null}} [options]
 *
 * @returns Promise<Response&{data?: Object}>
 */
export async function fetch(url, options = {}) {
    /**
     * @type {{url: (RequestInfo|URL), options: (RequestInit|{params?: Object}), next: Promise<void>}}
     */
    const payload = {
        url,
        options,
        next: null,
    };

    fetchBus.trigger('fetch:request', payload);

    if (payload.next) {
        await payload.next;
    }

    url = payload.url;
    options = payload.options;

    try {
        if ('params' in options) {
            const params = typeof options.params === 'object' ? new URLSearchParams(options.params) : options.params;
            const query = params.toString();

            if (query) {
                url += (url.includes('?') ? '&' : '?') + query;
            }
        }

        const headers = {...(options.headers || {})};
        let body = options.body;

        if ((typeof body === 'object' || typeof body === 'string') && !(body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';

            if (typeof body === 'object') {
                body = JSON.stringify(body);
            }
        }

        for (const [key, value] of Object.entries(headers)) {
            if ([undefined, null].includes(value)) {
                delete headers[key];
            }
        }

        const response = await window.fetch(url, {
            ...options,
            headers,
            body,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            throw new HttpError(response, response.statusText, errorData);
        }

        const contentType = response.headers.get('content-type')?.split(';')[0].trim();

        if (contentType === 'application/json') {
            response.data = await response.json().catch(() => null);
        } else {
            response.data = null;
        }

        fetchBus.trigger('fetch:success', {url, options, response, data: response.data});

        return response;
    } catch (error) {
        const errorPayload = {
            url,
            options,
            error,
            next: Promise.reject(error),
        };

        if (error.name === "AbortError") {
            return Promise.resolve({data: {}});
        }

        fetchBus.trigger('fetch:error', errorPayload);

        return errorPayload.next;
    }
}
