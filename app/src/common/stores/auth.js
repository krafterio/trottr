import {defineStore} from 'pinia';
import {bus} from "@/common/composables/bus";
import {fetch} from "@/common/network/fetch";
import {setDefaultAuthorization} from "@/common/plugins/fetcher";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        token: localStorage.getItem('token'),
        refreshToken: localStorage.getItem('refreshToken'),
        isAuthenticated: !!localStorage.getItem('token'),
        loading: false,
        error: null,
        tokenExpiration: localStorage.getItem('tokenExpiration') ? parseInt(localStorage.getItem('tokenExpiration')) : null,
    }),

    getters: {
        currentUser: (state) => state.user,
        isTokenExpired: (state) => {
            if (!state.tokenExpiration) return true
            return Date.now() > state.tokenExpiration
        },
        canRefreshToken: (state) => state.isAuthenticated && !!state.refreshToken,
    },

    actions: {
        async login(credentials) {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch(`/auth/token`, {
                    method: 'POST',
                    body: credentials,
                });
                return response.data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Erreur de connexion';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        setTokens(accessToken, refreshToken, expiresIn) {
            this.token = accessToken;
            this.refreshToken = refreshToken;
            this.isAuthenticated = true;

            // Store the expiration time (timestamp in milliseconds)
            const expirationTime = Date.now() + (expiresIn * 1000);
            this.tokenExpiration = expirationTime;

            // Save to localStorage
            localStorage.setItem('token', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
            localStorage.setItem('tokenExpiration', expirationTime.toString());

            // Update the Authorization header for fetch
            setDefaultAuthorization(accessToken);
        },

        async refreshAccessToken() {
            if (!this.refreshToken) {
                this.logout().then();
                return false;
            }

            try {
                const response = await fetch(`/auth/refresh`, {
                    method: 'POST',
                    body: {
                        refresh_token: this.refreshToken,
                    },
                })

                this.setTokens(
                    response.data.access_token,
                    response.data.refresh_token,
                    response.data.expires_in,
                )

                return true;
            } catch (error) {
                this.logout();
                return false;
            }
        },

        async register(userData) {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch(`/auth/register`, {
                    method: 'POST',
                    body: userData,
                });
                return response.data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Erreur lors de l\'inscription';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async requestPasswordReset(data) {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch(`/auth/password-reset-request`, {
                    method: 'POST',
                    body: data,
                });

                return response.data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Erreur lors de la demande de réinitialisation';

                throw error;
            } finally {
                this.loading = false;
            }
        },

        async confirmPasswordReset(data) {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch(`/auth/password-reset-confirm`, {
                    method: 'POST',
                    body: data,
                });

                return response.data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Erreur lors de la réinitialisation';

                throw error;
            } finally {
                this.loading = false;
            }
        },

        async verifyLoginCode(email, code) {
            this.loading = true;
            this.error = null;

            try {
                const response = await fetch(`/auth/verify-login-code`, {
                    method: 'POST',
                    body: {
                        email: email,
                        code: code
                    },
                });

                this.setTokens(
                    response.data.access_token,
                    response.data.refresh_token,
                    response.data.expires_in
                );

                await this.fetchUser();

                return response.data;
            } catch (error) {
                this.error = error.response?.data?.detail || 'Code de vérification invalide';
                throw error;
            } finally {
                this.loading = false;
            }
        },

        async fetchUser() {
            if (!this.token) {
                return;
            }

            // Check if the token is expired
            if (this.token && this.isTokenExpired) {
                const success = await this.refreshAccessToken();

                if (!success) {
                    return
                }
            }

            try {
                const response = await fetch(`/account`);
                this.user = response.data;
            } catch (error) {
                // If 401, let's try to refresh the token
                if (error.response?.status === 401) {
                    const success = await this.refreshAccessToken();

                    if (success) {
                        // Retry the request with the new token
                        const response = await fetch(`/account`);
                        this.user = response.data;
                    } else {
                        this.logout().then();
                        throw error;
                    }
                } else {
                    throw error;
                }
            }
        },

        async logout() {
            // Try to revoke the token on the server
            if (this.refreshToken) {
                try {
                    await fetch(`/auth/logout`, {
                        method: 'POST',
                        body: {
                            refresh_token: this.refreshToken,
                        },
                    })
                } catch (error) {
                    console.error('Error during server-side logout', error);
                }
            }

            this.user = null;
            this.token = null;
            this.refreshToken = null;
            this.tokenExpiration = null;
            this.isAuthenticated = false;

            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('tokenExpiration');

            setDefaultAuthorization(null);

            bus.trigger('auth:logout');
        }
    }
});
