// Plugins
import VueSweetalert2 from "vue-sweetalert2"
import 'sweetalert2/dist/sweetalert2.min.css'

export function registerPlugins (app) {
  app
    .use(VueSweetalert2)
    .use(router)
}
