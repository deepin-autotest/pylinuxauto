---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: PyLinuxAuto
  text: Linux GUI Automation with Python
  tagline: Empower your RPA workflow with seamless Linux GUI automation, powered by Python.
  image:
    src: /logo.png
    alt: PyLinuxAuto

features:
  - icon: 🖥️
    title: 专注于 Linux GUI 自动化
    details: 支持多种元素定位方案，完美支持 Linux GUI 自动化。
  - icon: 🐍
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
  {
    avatar: 'https://www.github.com/qisijia367.png',
    name: 'qisijia367',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/qisijia367' },
    ]
  },
  {
    avatar: 'https://www.github.com/KeyLee123.png',
    name: 'KeyLee123',
    title: 'Developer',
    links: [
      { icon: 'github', link: 'https://github.com/KeyLee123' },
    ]
  },
]

</script>


<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>
      Contributors
    </template>
  </VPTeamPageTitle>
  <VPTeamMembers
    size="small"
    :members="members"
  />
</VPTeamPage>
