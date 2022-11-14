import {createStore} from 'vuex'

export default createStore({
    state: {
        isAuthenticated: false,
        access: '',
        refresh: '',
        isLoading: false,
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('access') && localStorage.getItem('refresh')) {
                state.access = localStorage.getItem('access')
                state.refresh = localStorage.getItem('refresh')
            } else {
                state.access = ''
                state.refresh = ''
                state.isAuthenticated = false
            }
        },
        setIsLoading(state, status) {
            state.isLoading = status
        },
        setToken(state, access, refresh) {
            state.access = access
            state.refresh = refresh
            state.isAuthenticated = true
        },
        removeToken(state) {
            state.access = ''
            state.refresh = ''
            state.isAuthenticated = false
        },

        removeTokenFromStorage(state) {
            localStorage.removeItem('refresh')
            localStorage.removeItem('access')
        }
    },
    actions: {},
    modules: {}
})