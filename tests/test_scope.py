# Copyright (c) 2017 The OpenTracing Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import

import mock

from opentracing.scope_manager import ScopeManager
from opentracing.tracer import Tracer
from opentracing.scope import Scope
from opentracing.span import Span, SpanContext


def test_scope_wrapper():
    # ensure `Scope` wraps the `Span` argument
    span = Span(tracer=Tracer(), context=SpanContext())
    scope = Scope(ScopeManager, span, finish_on_close=False)
    assert scope.span() == span


def test_scope_context_manager():
    # ensure `Scope` can be used in a Context Manager that
    # calls the `close()` method
    span = Span(tracer=Tracer(), context=SpanContext())
    scope = Scope(ScopeManager(), span)
    with mock.patch.object(scope, 'close') as close:
        with scope:
            pass
        assert close.call_count == 1
