import {defineConfig} from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
    base: process.env.VITE_BASE,
    lang: 'zh-CN',
    title: "PyLinuxAuto | 让 Linux GUI 自动化测试变得更简单",
    description: "Linux GUI Automation with Python",
    head: [
        // ['meta', {name: 'referrer', content: 'no-referrer-when-downgrade'}],
        ['link', {rel: 'icon', href: `${process.env.VITE_BASE || '/'}favicon.ico`}],
    ],
    vite: {
        publicDir: "assets",
    },

    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        siteTitle: "PyLinuxAuto",
        nav: [
            {text: '🏠 首页', link: '/index'},
            {text: '🧭 指南', link: '/指南/README'},
        ],

        sidebar: {
             "/指南/": [
                {
                    text: "PyLinuxAuto",
                    items: [
                        {text: "简介", link: "/指南/README"},
                    ]
                },
                {
                    text: "详细内容",
                    items: [
                        {text: "属性定位", link: "/指南/属性定位"},
                        {text: "图像识别", link: "/指南/图像识别"},
                        {text: "OCR识别", link: "/指南/OCR识别"},
                        {text: "相对位移定位", link: "/指南/相对位移定位"},
                        {text: "问题", link: "/指南/问题"},
                    ]
                },
            ],
        },
        search: {
            provider: 'local'
        },
        ignoreDeadLinks: true,
        // =========================================================
        logo: {src: '/logo.png', width: 22, height: 30},
        socialLinks: [
            {icon: 'github', link: 'https://github.com/funny-dream/pylinuxauto'}
        ],
        footer: {
            copyright: `版权所有 © 2024-${new Date().getFullYear()} 统信软件`
        },
        //大纲显示2-3级标题
        outline: [2, 4],
        //大纲顶部标题
        outlineTitle: '当前页大纲',

        docFooter: {
            prev: '上一页',
            next: '下一页'
        },

        lastUpdated: {
            text: '最后更新于',
            formatOptions: {
                dateStyle: 'short',
                timeStyle: 'medium'
            }
        },

        langMenuLabel: '多语言',
        returnToTopLabel: '回到顶部',
        sidebarMenuLabel: '菜单',
        darkModeSwitchLabel: '主题',
        lightModeSwitchTitle: '切换到浅色模式',
        darkModeSwitchTitle: '切换到深色模式'
    },
});
