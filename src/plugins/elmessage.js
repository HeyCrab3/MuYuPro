// 注入 Element Plus 的 ElMessage 类
// Vuetify3 的 Snackbar 是坨狗屎
import { ElMessage } from 'element-plus'
import 'element-plus/es/components/message/style/css'
export function registerPlugins (app) {
    app
      .use(ElMessage)
  }