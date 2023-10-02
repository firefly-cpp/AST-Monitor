# ast-map

This is the instruction for developing the user interface of the map plugin for AST-Monitor. The map plugin is developed
in [Vue 3](https://vuejs.org/). This plugin allows display of current location on a map.

## Current features

- ✅ Speed display
- ✅ Distance display
- ✅ Heartrate display
- ✅ Map and GPS location display
- ✅ Duration display
- ✅ To-go Ascent display
- ✅ To-go Distance display
- ✅ Route progress
- ✅ Route display

## Partially implemented features

- 🚧 Route import feature

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for
type checking. In editors, we
need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)
to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented
a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more
performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1) Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2) Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

The dist folder is served inside the AST-Monitor map display, which is rendered
by [PyQt6 WebEngineView](https://doc.qt.io/qt-6/qwebengineview.html). If you update anything always run

```sh
npm run build
``` 


