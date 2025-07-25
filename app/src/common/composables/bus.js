import {onMounted, onBeforeUnmount} from 'vue';

export class EventBus extends EventTarget {
    trigger(name, payload) {
        this.dispatchEvent(new CustomEvent(name, {detail: payload}));
    }
}

export const bus = new EventBus();

/**
 * Ensures a bus event listener is attached and cleared the proper way.
 *
 * @param {EventBus} bus
 * @param {string} eventName
 * @param {EventListener} callback
 */
export function useBus(bus, eventName, callback) {
    onMounted(() => {
        bus.addEventListener(eventName, callback);
    });

    onBeforeUnmount(() => {
        bus.removeEventListener(eventName, callback);
    });
}