let observeFunction = null;

export function observe(func)
{
    observeFunction = func;
    func();
    observeFunction = null;
}

export function observer(obj)
{
    const observers = {};

    return new Proxy(obj, {
        get(target, prop)
        {
            if (observeFunction !== null) {
                if (!(prop in observers)) {
                    observers[prop] = new Set();
                }
                observers[prop].add(observeFunction);
            }
            return target[prop];
        },
        set(target, prop, val)
        {
            if (target[prop] === val || JSON.stringify(target[prop]) === JSON.stringify(val)) {
                return true;
            }
            target[prop] = val;
            if (prop in observers) {
                observers[prop].forEach(func => func());
            }
            return true;
        }
    })
}