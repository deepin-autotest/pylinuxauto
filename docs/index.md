---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: PyLinuxAuto
  text: 让 Linux GUI 自动化测试变得更简单
  tagline: Linux GUI Automation with Python
  actions:
    - theme: brand
      text: GitHub
      link: "https://github.com/funny-dream/pylinuxauto"
    - theme: alt
      text: Issues
      link: "https://github.com/funny-dream/pylinuxauto/issues"
  image:
    src: /logo.png
    alt: PyLinuxAuto

features:
  - icon: 🖥️
    title: 专注于 Linux GUI 自动化测试
    details: 支持多种元素定位方案，完美支持 Linux GUI 自动化测试。
  - icon: 📖
    title: 纯 Python 接口，轻量化依赖
    details: 统一的 Python 调用接口，使用简单方便，环境依赖少。

---


<script setup>
import {
  VPTeamPage,
  VPTeamPageTitle,
  VPTeamMembers
} from 'vitepress/theme'

const members = [
  {
    avatar: 'https://www.github.com/mikigo.png',
    name: 'mikigo',
    title: 'Creator',
    org: 'PyLinuxAuto',
    orgLink: 'https://github.com/funny-dream/pylinuxauto',
    links: [
      { icon: 'github', link: 'https://github.com/mikigo' },
      { icon: 'x', link: 'https://twitter.com/mikigo_' },
    ]
  },
]

</script>


<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>
      Contributors
    </template>
    <template #lead>
      感谢以下所有人的贡献与参与
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="members"
  />
</VPTeamPage>
