import {resolveDynamicComponent} from "vue";

export function hasProps(component, propName) {
  return resolveDynamicComponent(component)?.props?.[propName] !== undefined;
}
