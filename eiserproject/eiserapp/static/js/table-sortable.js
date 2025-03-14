/*
 * table-sortable
 * version: 2.0.3
 * release date: 4/2/2021
 * (c) Ravi Dhiman <ravi.dhiman@ravid.dev> https://ravid.dev
 * For the full copyright and license information, please view the LICENSE
 */
! function(t) {
    var e = {};

    function n(a) {
        if (e[a]) return e[a].exports;
        var i = e[a] = {
            i: a,
            l: !1,
            exports: {}
        };
        return t[a].call(i.exports, i, i.exports, n), i.l = !0, i.exports
    }
    n.m = t, n.c = e, n.d = function(t, e, a) {
        n.o(t, e) || Object.defineProperty(t, e, {
            enumerable: !0,
            get: a
        })
    }, n.r = function(t) {
        "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(t, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(t, "__esModule", {
            value: !0
        })
    }, n.t = function(t, e) {
        if (1 & e && (t = n(t)), 8 & e) return t;
        if (4 & e && "object" === typeof t && t && t.__esModule) return t;
        var a = Object.create(null);
        if (n.r(a), Object.defineProperty(a, "default", {
                enumerable: !0,
                value: t
            }), 2 & e && "string" != typeof t)
            for (var i in t) n.d(a, i, function(e) {
                return t[e]
            }.bind(null, i));
        return a
    }, n.n = function(t) {
        var e = t && t.__esModule ? function() {
            return t.default
        } : function() {
            return t
        };
        return n.d(e, "a", e), e
    }, n.o = function(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }, n.p = "", n(n.s = 1)
}([function(t, e) {
    t.exports = jQuery
}, function(t, e, n) {
    t.exports = n(3)
}, function(t, e, n) {}, function(t, e, n) {
    "use strict";
    n.r(e);
    var a = {};

    function i(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function r(t, e) {
        for (var n = 0; n < e.length; n++) {
            var a = e[n];
            a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
        }
    }

    function o(t, e, n) {
        return e && r(t.prototype, e), n && r(t, n), t
    }
    n.r(a), n.d(a, "_isArray", (function() {
        return c
    })), n.d(a, "_isNumber", (function() {
        return h
    })), n.d(a, "_isObject", (function() {
        return d
    })), n.d(a, "_isFunction", (function() {
        return f
    })), n.d(a, "_isString", (function() {
        return p
    })), n.d(a, "_isDate", (function() {
        return g
    })), n.d(a, "_sort", (function() {
        return _
    })), n.d(a, "_keys", (function() {
        return m
    })), n.d(a, "_forEach", (function() {
        return b
    })), n.d(a, "_filter", (function() {
        return v
    })), n.d(a, "_invariant", (function() {
        return y
    })), n.d(a, "_nativeCompare", (function() {
        return P
    })), n.d(a, "debounce", (function() {
        return k
    })), n.d(a, "_lower", (function() {
        return C
    })), n.d(a, "lookInObject", (function() {
        return E
    })), n.d(a, "_inRange", (function() {
        return w
    }));
    var s, l = n(0),
        u = n.n(l),
        c = function(t) {
            return Array.isArray(t)
        },
        h = function(t) {
            return "number" === typeof t && !isNaN(t)
        },
        d = function(t) {
            return "object" === typeof t
        },
        f = function(t) {
            return "function" === typeof t
        },
        p = function(t) {
            return "string" === typeof t
        },
        g = function(t) {
            if ("[object Date]" === Object.prototype.toString.call(t) && !isNaN(t)) return !0;
            if (p(t)) {
                var e = new Date(t);
                if (h(e.getDate())) return !0
            }
            return !1
        },
        _ = function(t, e) {
            return t.sort((function(t, n) {
                return "asc" === e ? parseInt(t, 10) - parseInt(n, 10) : parseInt(n, 10) - parseInt(t, 10)
            }))
        },
        m = function(t) {
            return "keys" in Object ? Object.keys(t) : Object.getOwnPropertyNames(t)
        },
        b = function(t, e) {
            if (y(c(t), "ForEach requires array input"), !t.length) return [];
            f(e) || (e = function() {});
            for (var n = 0, a = t.length; n < a;) e.apply(null, [t[n], n]), n += 1;
            return t
        },
        v = function(t, e) {
            if (y(c(t), "_filter requires array input"), !t.length) return [];
            if (!f(e)) return t;
            for (var n = 0, a = t.length, i = []; n < a;) e.apply(null, [t[n], n]) && i.push(t[n]), n += 1;
            return i
        },
        y = function(t, e) {
            var n;
            if (!t) {
                for (var a = arguments.length, i = new Array(a > 2 ? a - 2 : 0), r = 2; r < a; r++) i[r - 2] = arguments[r];
                var o = [].concat(i),
                    s = 0;
                throw (n = new Error(e.replace(/%s/g, (function() {
                    return o[s++]
                })))).name = "TableSortable Violation", n.framesToPop = 1, n
            }
        },
        P = function(t, e) {
            if (t !== e) {
                if (h(t)) return parseFloat(t) > parseFloat(e) ? 1 : -1;
                if (g(t)) {
                    var n = new Date(t),
                        a = new Date(e);
                    return n.getTime() > a.getTime() ? 1 : -1
                }
                return p(t) ? t > e ? 1 : -1 : 1
            }
            return 0
        },
        k = function(t, e) {
            var n;
            return function() {
                var a = this,
                    i = arguments;
                clearTimeout(n), n = window.setTimeout((function() {
                    return t.apply(a, i)
                }), e)
            }
        },
        C = function(t) {
            return p(t) ? t.toLowerCase() : String(t)
        },
        E = function(t, e) {
            var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : [];
            if (!e && !h(e)) return !1;
            var a = m(t);
            c(n) || (n = a);
            for (var i = 0, r = a.length, o = !1, s = C(e); i < r;) {
                var l = a[i],
                    u = C(t[l]);
                if (n.length && n.indexOf(l) > -1 && u.indexOf(s) > -1) {
                    o = !0;
                    break
                }
                if (!n.length && u.indexOf(s) > -1) {
                    o = !0;
                    break
                }
                i += 1
            }
            return o
        },
        w = function(t, e) {
            return c(e) && e[0] <= t && e[1] > t
        },
        D = function() {
            function t() {
                i(this, t), this._name = "dataset", this.dataset = null, this._cachedData = null, this._datasetLen = 0, this._outLen = 10, this.sortDirection = {
                    ASC: "asc",
                    DESC: "desc"
                }
            }
            return o(t, [{
                key: "_formatError",
                value: function(t, e, n) {
                    for (var i = arguments.length, r = new Array(i > 3 ? i - 3 : 0), o = 3; o < i; o++) r[o - 3] = arguments[o];
                    y.apply(a, [t, "".concat(this._name, ".").concat(e, " ").concat(n)].concat(r))
                }
            }, {
                key: "_hasDataset",
                value: function() {
                    this._formatError(null !== this.dataset, "data", 'No source collection is provided. Add your collection to dataset with "dataset.fromCollection([{}])" method.')
                }
            }, {
                key: "fromCollection",
                value: function(t) {
                    this._formatError(c(t), "fromCollection", "Requires dataset to be a collection, like [{ }]"), this.dataset = t, this._cachedData = JSON.stringify(t), this._datasetLen = t.length
                }
            }, {
                key: "top",
                value: function(t) {
                    return this._hasDataset(), t ? (this._formatError(h(t), "top", "Requires length to be a number"), this.dataset.slice(0, t)) : this.dataset.slice(0, this._outLen)
                }
            }, {
                key: "bottom",
                value: function(t) {
                    return this._hasDataset(), t ? (this._formatError(h(t), "bottom", "Requires length to be a number"), t = Math.max(this._datasetLen - t, 0), this.dataset.slice(t, this._datasetLen)) : (t = Math.max(this._datasetLen - this._outLen, 0), this.dataset.slice(t, this._datasetLen))
                }
            }, {
                key: "get",
                value: function(t, e) {
                    return this._hasDataset(), this._formatError(h(t), "get", 'Requires "from" to be a number'), this._formatError(h(e), "get", 'Requires "to" to be a number'), this._formatError(!(t > e), "get", '"from" cannot be greater than "to"'), t = Math.max(t, 0), e = Math.min(e, this._datasetLen), this.dataset.slice(t, e)
                }
            }, {
                key: "sort",
                value: function(t, e) {
                    this._hasDataset(), this._formatError(p(t), "sort", 'Requires "column" type of string'), this._formatError(p(e), "sort", 'Requires "direction" type of string'), this._formatError("asc" === e || "desc" === e, "sort", '"%s" is invalid sort direction. Use "dataset.sortDirection.ASC" or "dataset.sortDirection.DESC".', e);
                    var n = this.top(1)[0];
                    return this._formatError("undefined" !== typeof n[t], "sort", 'Column name "%s" does not exist in collection', t), this.sortDirection.ASC === e ? this.dataset.sort((function(e, n) {
                        return P(e[t], n[t])
                    })) : this.dataset.sort((function(e, n) {
                        return P(n[t], e[t])
                    })), this.top(this._datasetLen)
                }
            }, {
                key: "pushData",
                value: function(t) {
                    c(t) && Array.prototype.push.apply(this.dataset, t)
                }
            }, {
                key: "lookUp",
                value: function(t, e) {
                    if (p(t) || h(t)) {
                        var n = JSON.parse(this._cachedData);
                        this.dataset = "" === t ? n : v(n, (function(n) {
                            return E(n, t, e)
                        })), this._datasetLen = this.dataset.length
                    }
                }
            }]), t
        }(),
        x = function(t, e, n) {
            return {
                node: t,
                attrs: e,
                children: n
            }
        },
        S = function(t) {
            var e = t.node,
                n = t.attrs;
            t.children;
            return function(t, e) {
                if (!e) return t;
                for (var n = Object.keys(e), a = 0; a < n.length;) {
                    var i = n[a],
                        r = e[i];
                    void 0 !== r && (/^on/.test(i) && r ? t.on(i.replace(/^on/, "").toLowerCase(), r) : "text" === i ? t.text(r) : "html" === i ? t.html(r) : "append" === i ? t.append(r) : "className" === i ? t.attr("class", r) : t.attr(i, r), a += 1)
                }
                return t
            }(u()("<".concat(e, "></").concat(e, ">")), n)
        },
        U = function t(e, n, a) {
            if (a || n.empty(), c(e)) {
                for (var i = [], r = 0; r < e.length; r++) {
                    var o = S(e[r]);
                    e[r].children && (o = t(e[r].children, o, !0)), i.push(o)
                }
                n.append(i)
            } else if (d(e)) {
                var s = S(e);
                e.children && (s = t(e.children, s, !0)), n.append(s)
            }
            return n
        },
        L = function() {
            return {
                createElement: x,
                render: U
            }
        },
        O = (n(2), function() {
            function t(e) {
                var n = this;
                i(this, t), this._name = "tableSortable", this._defOptions = {
                    element: "",
                    data: [],
                    columns: {},
                    sorting: !0,
                    pagination: !0,
                    paginationContainer: null,
                    rowsPerPage: 10,
                    formatCell: null,
                    formatHeader: null,
                    searchField: null,
                    responsive: {},
                    totalPages: 0,
                    sortingIcons: {
                        asc: "<span>\u25bc</span>",
                        desc: "<span>\u25b2</span>"
                    },
                    nextText: "<span>Next</span>",
                    prevText: "<span>Prev</span>",
                    tableWillMount: function() {},
                    tableDidMount: function() {},
                    tableWillUpdate: function() {},
                    tableDidUpdate: function() {},
                    tableWillUnmount: function() {},
                    tableDidUnmount: function() {},
                    onPaginationChange: null
                }, this._styles = null, this._dataset = null, this._table = null, this._thead = null, this._tbody = null, this._isMounted = !1, this._isUpdating = !1, this._sorting = {
                    currentCol: "",
                    dir: ""
                }, this._pagination = {
                    elm: null,
                    currentPage: 0,
                    totalPages: 1,
                    visiblePageNumbers: 5
                }, this._cachedOption = null, this._cachedViewPort = -1, this.setData = function(t, e, a) {
                    n.logError(c(t), "setData", "expect first argument as array of objects"), n.logError(d(e), "setData", "expect second argument as objects"), n._isMounted && t && (a ? n._dataset.pushData(t) : n._dataset.fromCollection(t), e && (n.options.columns = e), n.refresh())
                }, this.getData = function() {
                    return n._isMounted ? n._dataset.top() : []
                }, this.getCurrentPageData = function() {
                    if (n._isMounted) {
                        var t = n.options.rowsPerPage,
                            e = n._pagination.currentPage * t,
                            a = e + t;
                        return n._dataset.get(e, a)
                    }
                    return []
                }, this.refresh = function(t) {
                    t ? (n.distroy(), n.create()) : n._isMounted && n.updateTable()
                }, this.distroy = function() {
                    n._isMounted && (n.emitLifeCycles("tableWillUnmount"), n._table.remove(), n._styles && n._styles.length && (n._styles.remove(), n._styles = null), n._dataset = null, n._table = null, n._thead = null, n._tbody = null, n._pagination.elm && n._pagination.elm.remove(), n._pagination = {
                        elm: null,
                        currentPage: 0,
                        totalPages: 0,
                        visiblePageNumbers: 5
                    }, n._isMounted = !1, n._isUpdating = !1, n._sorting = {
                        currentCol: "",
                        dir: ""
                    }, n._cachedViewPort = -1, n._cachedOption = null, n.emitLifeCycles("tableDidUnmount"))
                }, this.create = function() {
                    n._isMounted || n.init()
                }, this.options = u.a.extend(this._defOptions, e), delete this._defOptions, this._rootElement = u()(this.options.element), this.engine = L(), this.optionDepreciation(), this.init(), this._debounceUpdateTable()
            }
            return o(t, [{
                key: "optionDepreciation",
                value: function() {
                    var t = this.options;
                    this.logWarn(t.columnsHtml, "columnsHtml", "has been deprecated. Use formatHeader()"), this.logWarn(t.processHtml, "processHtml", "has been deprecated. Use formatCell()"), this.logWarn(t.dateParsing, "dateParsing", "has been deprecated. It is true by default."), this.logWarn(t.generateUniqueIds, "generateUniqueIds", "has been deprecated. It is true by default."), this.logWarn(t.showPaginationLabel, "showPaginationLabel", "has been deprecated. It is true by default."), this.logWarn(t.paginationLength, "paginationLength", "has been deprecated. Use rowsPerPage")
                }
            }, {
                key: "logError",
                value: function(t, e, n) {
                    for (var i = arguments.length, r = new Array(i > 3 ? i - 3 : 0), o = 3; o < i; o++) r[o - 3] = arguments[o];
                    y.apply(a, [t, "".concat(this._name, ".").concat(e, " ").concat(n)].concat(r))
                }
            }, {
                key: "logWarn",
                value: function(t, e, n) {
                    t && console.warn("".concat(this._name, ".options.").concat(e, " ").concat(n))
                }
            }, {
                key: "emitLifeCycles",
                value: function(t) {
                    if (this.options) {
                        var e = this.options;
                        if (f(e[t])) {
                            for (var n = arguments.length, a = new Array(n > 1 ? n - 1 : 0), i = 1; i < n; i++) a[i - 1] = arguments[i];
                            e[t].apply(this, a)
                        }
                    }
                }
            }, {
                key: "setPage",
                value: function(t, e) {
                    this.logError(h(t), "setPage", "expect argument as number");
                    var n = this._pagination.totalPages;
                    h(t) && w(t, [0, n]) && (this._pagination.currentPage = t, e && this._dataset.pushData(e), this.updateTable())
                }
            }, {
                key: "updateRowsPerPage",
                value: function(t) {
                    this.logError(h(t), "updateRowsPerPage", "expect argument as number"), t && (this._pagination.currentPage = 0, this.options.rowsPerPage = t, this.updateTable())
                }
            }, {
                key: "lookUp",
                value: function(t) {
                    var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : [],
                        n = this.options.columns;
                    this.logError(e && c(e), "lookUp", "second argument must be array of keys"), e.length || (e = n), this._pagination.currentPage = 0, this._dataset.lookUp(t, m(e)), this.debounceUpdateTable()
                }
            }, {
                key: "_bindSearchField",
                value: function() {
                    var t = this,
                        e = this.options.searchField;
                    if (e) {
                        var n = u()(e);
                        this.logError(n.length, "searchField", '"%s" is not a valid DOM element or string', n), n.on("input", (function() {
                            var e = u()(this).val();
                            t.lookUp(e)
                        })), this.options.searchField = n
                    }
                }
            }, {
                key: "_validateRootElement",
                value: function() {
                    this.logError(this._rootElement.length, "element", '"%s" is not a valid root element', this._rootElement)
                }
            }, {
                key: "_createTable",
                value: function() {
                    this._table = u()("<table></table>").addClass("table gs-table")
                }
            }, {
                key: "_initDataset",
                value: function() {
                    var t = this.options.data;
                    this.logError(c(t), "data", "table-sortable only supports collections. Like: [{ key: value }, { key: value }]");
                    var e = new D;
                    e.fromCollection(t), this._dataset = e
                }
            }, {
                key: "_validateColumns",
                value: function() {
                    var t = this.options.columns;
                    this.logError(d(t), "columns", "Invalid column type, see docs")
                }
            }, {
                key: "sortData",
                value: function(t) {
                    var e = this._sorting,
                        n = e.dir,
                        a = e.currentCol;
                    t !== a && (n = ""), n ? n === this._dataset.sortDirection.ASC ? n = this._dataset.sortDirection.DESC : n === this._dataset.sortDirection.DESC && (n = this._dataset.sortDirection.ASC) : n = this._dataset.sortDirection.ASC, a = t, this._sorting = {
                        dir: n,
                        currentCol: a
                    }, this._dataset.sort(a, n), this.updateCellHeader()
                }
            }, {
                key: "_addColSorting",
                value: function(t, e) {
                    var n = this,
                        a = this.options.sorting,
                        i = this;
                    return a ? (a && !c(a) && ((t = u()(t)).attr("role", "button"), t.addClass("gs-button"), e === this._sorting.currentCol && this._sorting.dir && t.append(this.options.sortingIcons[this._sorting.dir]), t.click((function(t) {
                        i.sortData(e)
                    }))), c(a) && b(a, (function(a) {
                        e === a && ((t = u()(t)).attr("role", "button"), t.addClass("gs-button"), e === n._sorting.currentCol && n._sorting.dir && t.append(n.options.sortingIcons[n._sorting.dir]), t.click((function(t) {
                            i.sortData(e)
                        })))
                    })), t) : t
                }
            }, {
                key: "getCurrentPageIndex",
                value: function() {
                    var t = this._dataset._datasetLen,
                        e = this.options,
                        n = e.pagination,
                        a = e.rowsPerPage,
                        i = this._pagination.currentPage;
                    if (!n) return {
                        from: 0
                    };
                    var r = i * a,
                        o = Math.min(r + a, t);
                    return {
                        from: r = Math.min(r, o),
                        to: o
                    }
                }
            }, {
                key: "_renderHeader",
                value: function(t) {
                    var e = this;
                    t || (t = u()('<thead class="gs-table-head"></thead>'));
                    var n = this.options,
                        a = n.columns,
                        i = n.formatHeader,
                        r = [],
                        o = m(a);
                    b(o, (function(t, n) {
                        var o = a[t];
                        f(i) && (o = i(a[t], t, n)), o = e._addColSorting(u()("<span></span>").html(o), t);
                        var s = e.engine.createElement("th", {
                            html: o
                        });
                        r.push(s)
                    }));
                    var s = this.engine.createElement("tr", null, r);
                    return this.engine.render(s, t)
                }
            }, {
                key: "_renderBody",
                value: function(t) {
                    t || (t = u()('<tbody class="gs-table-body"></tbody>'));
                    var e = this.engine,
                        n = this.options,
                        a = n.columns,
                        i = n.formatCell,
                        r = this.getCurrentPageIndex(),
                        o = r.from,
                        s = r.to,
                        l = [];
                    l = void 0 === s ? this._dataset.top() : this._dataset.get(o, s);
                    var c = [],
                        h = m(a);
                    return b(l, (function(t, n) {
                        var a = [];
                        b(h, (function(n) {
                            var r;
                            void 0 !== t[n] && (r = f(i) ? e.createElement("td", {
                                html: i(t, n)
                            }) : e.createElement("td", {
                                html: t[n]
                            }), a.push(r))
                        })), c.push(e.createElement("tr", null, a))
                    })), e.render(c, t)
                }
            }, {
                key: "_createCells",
                value: function() {
                    return {
                        thead: this._renderHeader(),
                        tbody: this._renderBody()
                    }
                }
            }, {
                key: "onPaginationBtnClick",
                value: function(t, e) {
                    var n = this,
                        a = this._pagination,
                        i = a.totalPages,
                        r = a.currentPage,
                        o = this.options.onPaginationChange;
                    "up" === t ? r < i - 1 && (r += 1) : "down" === t && r >= 0 && (r -= 1);
                    if (f(o)) {
                        var s = isNaN(e) ? r : e;
                        o.apply(this, [s, function(t) {
                            return n.setPage(t)
                        }])
                    } else this._pagination.currentPage = void 0 !== e ? e : r, this.updateTable()
                }
            }, {
                key: "renderPagination",
                value: function(t) {
                    var e = this,
                        n = this.engine,
                        a = this.options,
                        i = a.pagination,
                        r = a.paginationContainer,
                        o = a.prevText,
                        s = a.nextText,
                        l = this._pagination,
                        c = l.currentPage,
                        h = l.totalPages,
                        d = l.visiblePageNumbers,
                        f = Math.min(h, d),
                        p = 0,
                        g = Math.min(h, p + f);
                    if (c > f / 2 && c < h - f / 2 ? (p = c - Math.floor(f / 2), g = Math.min(h, p + f)) : c > h - f / 2 && (p = h - f, g = h), t || (t = u()('<div class="gs-pagination"></div>'), u()(r).length ? u()(r).append(t) : this._table.after(t)), !i) return t;
                    var _ = [],
                        m = n.createElement("button", {
                            className: "btn btn-default",
                            html: o,
                            disabled: 0 === c,
                            onClick: function() {
                                return e.onPaginationBtnClick("down")
                            }
                        });
                    _.push(m);
                    var b = n.createElement("button", {
                        className: "btn btn-default",
                        disabled: !0,
                        text: "..."
                    });
                    c > f / 2 && _.push(b);
                    for (var v = p; v < g;) {
                        var y = n.createElement("button", {
                            className: c === v ? "btn btn-primary active" : "btn btn-default",
                            onClick: function() {
                                var t = parseInt(u()(this).attr("data-page"), 10);
                                Number.isNaN(t) && (t = parseInt(u()(this).text() - 1)), e.onPaginationBtnClick(null, t)
                            },
                            text: v + 1,
                            "data-page": v
                        });
                        _.push(y), v += 1
                    }
                    c < h - f / 2 && _.push(b);
                    var P = n.createElement("button", {
                        className: "btn btn-default",
                        html: s,
                        disabled: c >= h - 1,
                        onClick: function() {
                            return e.onPaginationBtnClick("up")
                        }
                    });
                    _.push(P), t.append(_);
                    var k = this.getCurrentPageIndex(),
                        C = k.from,
                        E = k.to,
                        w = n.createElement("span", {
                            text: "Showing ".concat(Math.min(E, C + 1), " to ").concat(E, " of ").concat(this._dataset._datasetLen, " rows")
                        }),
                        D = n.createElement("div", {
                            className: "col-md-6"
                        }, w),
                        x = n.createElement("div", {
                            className: "btn-group d-flex justify-content-end"
                        }, _),
                        S = n.createElement("div", {
                            className: "col-md-6"
                        }, x),
                        U = n.createElement("div", {
                            className: "row"
                        }, [D, S]);
                    return n.render(U, t)
                }
            }, {
                key: "createPagination",
                value: function() {
                    var t = this.options,
                        e = t.rowsPerPage,
                        n = t.pagination,
                        a = t.totalPages;
                    if (!n) return !1;
                    this.logError(e && h(e), "rowsPerPage", "should be a number greater than zero."), this.logError(h(a), "totalPages", "should be a number greater than zero.");
                    var i = a || Math.ceil(this._dataset._datasetLen / e);
                    0 >= i && (i = 1), this._pagination.totalPages = i, this._pagination.elm ? this.renderPagination(this._pagination.elm) : this._pagination.elm = this.renderPagination()
                }
            }, {
                key: "_generateTable",
                value: function(t, e) {
                    this._table.html(""), this._table.append(t), this._table.append(e), this._thead = t, this._tbody = e
                }
            }, {
                key: "_renderTable",
                value: function() {
                    if (this._rootElement.is("table")) this._rootElement.html(this._table.html());
                    else {
                        var t = this.engine.createElement("div", {
                            className: "gs-table-container",
                            append: this._table
                        });
                        this._rootElement = this.engine.render(t, this._rootElement)
                    }
                }
            }, {
                key: "_initStyles",
                value: function() {
                    if (!this.options.responsive) {
                        var t = u()("<style></style>");
                        t.attr("id", "gs-table"), t.html(".gs-table-container .table{table-layout:fixed}@media(max-width:767px){.gs-table-container{overflow:auto;max-width:100%}}"), u()("head").append(t), this._styles = t
                    }
                }
            }, {
                key: "init",
                value: function() {
                    this.emitLifeCycles("tableWillMount"), this._validateRootElement(), this._initDataset(), this._createTable(), this._validateColumns();
                    var t = this._createCells(),
                        e = t.thead,
                        n = t.tbody;
                    this._generateTable(e, n), this._renderTable(), this.createPagination(), this._bindSearchField(), this._initStyles(), this._isMounted = !0, this.emitLifeCycles("tableDidMount"), -1 === this._cachedViewPort && this.resizeSideEffect()
                }
            }, {
                key: "_debounceUpdateTable",
                value: function() {
                    this.debounceUpdateTable = k(this.updateTable, 400)
                }
            }, {
                key: "updateTable",
                value: function() {
                    this._isUpdating || (this.emitLifeCycles("tableWillUpdate"), this._isUpdating = !0, this._renderHeader(this._thead), this._renderBody(this._tbody), this.createPagination(), this._isUpdating = !1, this.emitLifeCycles("tableDidUpdate"))
                }
            }, {
                key: "updateCellHeader",
                value: function() {
                    this._isUpdating || (this._isUpdating = !0, this.emitLifeCycles("tableWillUpdate"), this._renderHeader(this._thead), this._renderBody(this._tbody), this._isUpdating = !1, this.emitLifeCycles("tableDidUpdate"))
                }
            }, {
                key: "resizeSideEffect",
                value: function() {
                    var t = k(this.makeResponsive, 500);
                    window.addEventListener("resize", t.bind(this)), this.makeResponsive()
                }
            }, {
                key: "makeResponsive",
                value: function() {
                    var t, e = this.options.responsive,
                        n = window.innerWidth,
                        a = _(m(e), "desc");
                    if (this.logError(d(e), "responsive", 'Invalid type of responsive option provided: "%s"', e), b(a, (function(e) {
                            parseInt(e, 10) > n && (t = e)
                        })), this._cachedViewPort !== t) {
                        this._cachedViewPort = t;
                        var i = e[t];
                        d(i) ? (this._cachedOption || (this._cachedOption = u.a.extend({}, this.options)), this.options = u.a.extend(this.options, i), this.refresh()) : this._cachedOption && (this.options = u.a.extend({}, this._cachedOption), this._cachedOption = null, this._cachedViewPort = -1, this.refresh())
                    }
                }
            }]), t
        }());
    window.Pret = L(), window.TableSortable = O, window.DataSet = D, (s = jQuery).fn.tableSortable = function(t) {
        return t.element = s(this), new window.TableSortable(t)
    };
    e.default = O
}]);