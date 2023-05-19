/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
// F:\muyupro\node_modules\sweetalert2\dist\sweetalert2.min.css

// Plugins
import { registerPlugins } from '@/plugins'
import 'element-plus/es/components/message/style/css'
import 'element-plus/es/components/notification/style/css'
const app = createApp(App)

registerPlugins(app)

app.mount('#app')
