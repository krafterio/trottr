import {ref, onMounted} from 'vue';
import {fetch} from "@/common/network/fetch.js";

export default function useRecaptcha() {
    const isLoaded = ref(false);
    const isEnabled = ref(false);
    const siteKey = ref('');
    const isLoading = ref(true);
    const error = ref(null);

    const loadRecaptchaScript = () => {
        return new Promise((resolve, reject) => {
            if (window.grecaptcha) {
                isLoaded.value = true;

                return resolve();
            }

            if (!isEnabled.value) {
                return resolve();
            }

            const script = document.createElement('script');
            script.src = `https://www.google.com/recaptcha/api.js?render=${siteKey.value}`;
            script.async = true;
            script.defer = true;

            script.onload = () => {
                isLoaded.value = true;
                resolve();
            }

            script.onerror = (error) => {
                reject(error);
            }

            document.head.appendChild(script);
        })
    }

    const getToken = async (action) => {
        if (!isEnabled.value) {
            return null;
        }

        if (!isLoaded.value) {
            try {
                await loadRecaptchaScript();
            } catch (err) {
                error.value = 'Failed to load reCAPTCHA';
                return null;
            }
        }

        try {
            return await new Promise((resolve, reject) => {
                window.grecaptcha.ready(() => {
                    window.grecaptcha.execute(siteKey.value, {action})
                        .then(resolve)
                        .catch(reject);
                });
            });
        } catch (err) {
            error.value = 'Failed to get reCAPTCHA token';
            return null;
        }
    }

    const fetchConfig = async () => {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await fetch('/recaptcha/config');
            isEnabled.value = response.data.enabled;
            siteKey.value = response.data.site_key;

            if (isEnabled.value) {
                await loadRecaptchaScript();
            }
        } catch (err) {
            error.value = 'Failed to fetch reCAPTCHA configuration';
            console.error('reCAPTCHA config error:', err);
        } finally {
            isLoading.value = false;
        }
    }

    onMounted(() => {
        fetchConfig().then();
    });

    return {
        isEnabled,
        isLoaded,
        isLoading,
        error,
        getToken,
    };
}
