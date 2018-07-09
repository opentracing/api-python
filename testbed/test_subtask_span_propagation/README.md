# Subtask Span propagation example.

This example shows an active `Span` being simply propagated to the sutasks -either threads or coroutines-, and finished **by** the parent task. In real-life scenarios instrumentation libraries may help with `Span` propagation **if** not offered by default (see implementation details below), but we show here the case without such help.

Implementation details:
- For `threading`, `gevent` and `asyncio` the `Span` is manually passed down the call chain, being manually reactivated it in each corotuine/task.
- For `tornado`, the active `Span` is not passed nor activated down the chain as the custom `StackContext` automatically propagates it.

`threading` implementation:
```python
    def parent_task(self, message):
        with self.tracer.start_active_scope('parent') as scope:
            f = self.executor.submit(self.child_task, message, scope.span)
            res = f.result()

        return res

    def child_task(self, message, span):
        with self.tracer.scope_manager.activate(span, False):
            with self.tracer.start_active_scope('child'):
                return '%s::response' % message
```

`tornado` implementation:
```python
    def parent_task(self, message):
        with self.tracer.start_active_scope('parent'):
            res = yield self.child_task(message)

        raise gen.Return(res)

    @gen.coroutine
    def child_task(self, message):
        # No need to pass/activate the parent Span, as
        # it stays in the context.
        with self.tracer.start_active_scope('child'):
            raise gen.Return('%s::response' % message)
```
