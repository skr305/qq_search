import axios from 'axios'
import Qs from "qs"
// const baseURL = window.location.origin + "/"
// const baseURL = "/api/"


/** 生成一个固定模板的axios请求 */
export default ({url, params={}, method="POST", isFile=false}) => {

    return axios({
        url: url,
        method: method, // 默认是POST
        baseURL: process.env.NODE_ENV=== 'development' ? "/api/" : window.location.origin + "/",      
        // `headers` 是即将被发送的自定义请求头
        headers: 
        {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': isFile ? "multipart/form-data" : "application/x-www-form-urlencoded",
        },
      
        // `params` 是即将与请求一起发送的 URL 参数
        // 必须是一个无格式对象(plain object)或 URLSearchParams 对象
        params: params,
        
        /** django吃这一套 并且只吃Qs做的stringfy化的数据
         * 这个地方不能用params参数 得用data
         * 就相当于 postman里头的那个params和Body那里差不多
         * params只是写在url里头的 传输效果上和Body是不一样的
         * Django吃的是Body的那种 所以得用data参数
         * 配上Qs 这算是两个必要条件
         */
        data: params,
        withCredentials: true,
        // 在向服务器发送数据前将数据进行转换
        transformRequest: [function (data) {
            return Qs.stringify(data)
        }],
        
    })
}






