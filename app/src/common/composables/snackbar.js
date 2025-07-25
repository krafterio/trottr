import {reactive} from 'vue'

export function useSnackbar() {
    const snackbar = reactive({
        show: false,
        text: '',
        color: 'success'
    })

    const showSnackbar = (text, color = 'success') => {
        snackbar.text = text
        snackbar.color = color
        snackbar.show = true
    }

    return {
        snackbar,
        showSnackbar
    }
}
