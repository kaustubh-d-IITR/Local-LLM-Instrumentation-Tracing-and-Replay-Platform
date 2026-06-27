import { i as __toESM } from "../_runtime.mjs";
import { u as require_react } from "../_libs/@floating-ui/react-dom+[...].mjs";
import { s as require_jsx_runtime } from "../_libs/@radix-ui/react-arrow+[...].mjs";
import { c as useMetrics, i as useAttention, l as useTokens, n as useActivations, o as useCurrentSessionId, r as useAnomalies, s as useMemory, t as cn, u as useTopology } from "./utils-C2sR9Z8l.mjs";
import { M as useNavigate, h as Link } from "../_libs/@tanstack/react-router+[...].mjs";
import { a as ChevronDown, c as Activity, d as CircleX, i as ChevronUp, l as TriangleAlert, o as Check, r as Circle, s as ArrowLeft, t as Info } from "../_libs/lucide-react.mjs";
import { a as SelectItemIndicator, c as SelectPortal, d as SelectSeparator$1, f as SelectTrigger$1, i as SelectItem$1, l as SelectScrollDownButton$1, m as SelectViewport, n as SelectContent$1, o as SelectItemText, p as SelectValue$1, r as SelectIcon, s as SelectLabel$1, t as Select$1, u as SelectScrollUpButton$1 } from "../_libs/@radix-ui/react-select+[...].mjs";
import { a as YAxis, c as Area, d as PolarAngleAxis, f as PolarGrid, i as LineChart, l as Line, m as Tooltip, n as RadarChart, o as XAxis, p as ResponsiveContainer, r as BarChart, s as Bar, t as AreaChart, u as Radar } from "../_libs/recharts+[...].mjs";
import { i as Trigger, n as List, r as Root2, t as Content } from "../_libs/radix-ui__react-tabs.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/dashboard-DnXKjUOm.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
function Panel({ title, subtitle, actions, children, className, contentClassName }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
		className: cn("panel flex flex-col", className),
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("header", {
			className: "flex items-center justify-between gap-3 border-b border-border px-4 py-3",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "min-w-0",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
					className: "truncate text-sm font-semibold tracking-tight text-foreground",
					children: title
				}), subtitle && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "truncate text-xs text-muted-foreground",
					children: subtitle
				})]
			}), actions && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "shrink-0",
				children: actions
			})]
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: cn("flex-1 p-4", contentClassName),
			children
		})]
	});
}
var KIND_COLOR = {
	attn: "bg-[color:var(--color-info)]/20 text-[color:var(--color-info)] border-[color:var(--color-info)]/40",
	mlp: "bg-primary/15 text-primary border-primary/40",
	norm: "bg-muted text-muted-foreground border-border",
	embed: "bg-[color:var(--color-warning)]/15 text-[color:var(--color-warning)] border-[color:var(--color-warning)]/40"
};
function ModelTopology({ sessionId }) {
	const { data, isLoading, isError } = useTopology(sessionId);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
		title: "Model Topology",
		subtitle: data ? `${data.blocks?.length || 0} transformer blocks` : "Loading...",
		className: "h-full",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "max-h-[420px] space-y-1.5 overflow-auto pr-1",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "p-4 text-center text-sm text-muted-foreground",
					children: "Loading topology..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "p-4 text-center text-sm text-destructive",
					children: "Error loading topology"
				}),
				!isLoading && !isError && (!data?.blocks || data.blocks.length === 0) && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "p-4 text-center text-sm text-muted-foreground",
					children: "No topology data available."
				}),
				!isLoading && !isError && data?.blocks?.map((b, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "rounded-md border border-border bg-secondary/40 px-3 py-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "font-mono text-xs text-muted-foreground",
							children: b.name
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: cn("h-1.5 w-1.5 rounded-full", b.status === "ok" && "bg-[color:var(--color-success)]", b.status === "warn" && "bg-[color:var(--color-warning)]", b.status === "error" && "bg-destructive") })]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mt-1.5 flex flex-wrap gap-1",
						children: b.components?.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: cn("rounded border px-1.5 py-0.5 font-mono text-[10px]", KIND_COLOR[c.kind] || KIND_COLOR.norm),
							children: c.name
						}, c.name))
					})]
				}, b.index || i))
			]
		})
	});
}
function LiveExecutionStream({ sessionId }) {
	const { data, isLoading, isError } = useMetrics(sessionId);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
		title: "Live Execution Stream",
		subtitle: data ? `${data.length} events buffered` : "Waiting for stream...",
		className: "h-full",
		contentClassName: "p-0",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "max-h-[420px] overflow-auto font-mono text-[11px]",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "px-4 py-8 text-center text-muted-foreground",
					children: "Loading stream..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "px-4 py-8 text-center text-destructive",
					children: "Error loading execution stream."
				}),
				!isLoading && !isError && (!data || data.length === 0) && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "px-4 py-8 text-center text-muted-foreground",
					children: "Waiting for execution events…"
				}),
				!isLoading && !isError && data?.map((e) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: cn("flex items-center gap-2 border-b border-border/60 px-3 py-1.5", e.level === "warn" && "bg-[color:var(--color-warning)]/5", e.level === "error" && "bg-destructive/10"),
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: cn("h-1.5 w-1.5 shrink-0 rounded-full", e.level === "info" && "bg-[color:var(--color-success)]", e.level === "warn" && "bg-[color:var(--color-warning)]", e.level === "error" && "bg-destructive") }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "w-12 shrink-0 text-muted-foreground",
							children: ["L", e.layer.toString().padStart(2, "0")]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "w-20 shrink-0 truncate text-primary",
							children: e.op
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "w-14 shrink-0 text-right text-foreground",
							children: [e.dur_ms, "ms"]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "hidden flex-1 truncate text-muted-foreground sm:inline",
							children: e.shape
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "hidden w-12 shrink-0 text-muted-foreground md:inline",
							children: e.dtype
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "hidden w-14 shrink-0 text-muted-foreground md:inline",
							children: e.device
						})
					]
				}, e.id))
			]
		})
	});
}
var Select = Select$1;
var SelectValue = SelectValue$1;
var SelectTrigger = import_react.forwardRef(({ className, children, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SelectTrigger$1, {
	ref,
	className: cn("flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background cursor-pointer data-[placeholder]:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1", className),
	...props,
	children: [children, /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectIcon, {
		asChild: true,
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronDown, { className: "h-4 w-4 opacity-50" })
	})]
}));
SelectTrigger.displayName = SelectTrigger$1.displayName;
var SelectScrollUpButton = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectScrollUpButton$1, {
	ref,
	className: cn("flex cursor-default items-center justify-center py-1", className),
	...props,
	children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronUp, { className: "h-4 w-4" })
}));
SelectScrollUpButton.displayName = SelectScrollUpButton$1.displayName;
var SelectScrollDownButton = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectScrollDownButton$1, {
	ref,
	className: cn("flex cursor-default items-center justify-center py-1", className),
	...props,
	children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronDown, { className: "h-4 w-4" })
}));
SelectScrollDownButton.displayName = SelectScrollDownButton$1.displayName;
var SelectContent = import_react.forwardRef(({ className, children, position = "popper", ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectPortal, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SelectContent$1, {
	ref,
	className: cn("relative z-50 max-h-(--radix-select-content-available-height) min-w-[8rem] overflow-y-auto overflow-x-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-(--radix-select-content-transform-origin)", position === "popper" && "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1", className),
	position,
	...props,
	children: [
		/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectScrollUpButton, {}),
		/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectViewport, {
			className: cn("p-1", position === "popper" && "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]"),
			children
		}),
		/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectScrollDownButton, {})
	]
}) }));
SelectContent.displayName = SelectContent$1.displayName;
var SelectLabel = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectLabel$1, {
	ref,
	className: cn("px-2 py-1.5 text-sm font-semibold", className),
	...props
}));
SelectLabel.displayName = SelectLabel$1.displayName;
var SelectItem = import_react.forwardRef(({ className, children, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SelectItem$1, {
	ref,
	className: cn("relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50", className),
	...props,
	children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
		className: "absolute right-2 flex h-3.5 w-3.5 items-center justify-center",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectItemIndicator, { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Check, { className: "h-4 w-4" }) })
	}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectItemText, { children })]
}));
SelectItem.displayName = SelectItem$1.displayName;
var SelectSeparator = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectSeparator$1, {
	ref,
	className: cn("-mx-1 my-1 h-px bg-muted", className),
	...props
}));
SelectSeparator.displayName = SelectSeparator$1.displayName;
function AttentionHeatmap({ sessionId }) {
	const [layer, setLayer] = (0, import_react.useState)(0);
	const [head, setHead] = (0, import_react.useState)(0);
	const { data: topology } = useTopology(sessionId);
	const { data: attentions, isLoading, isError } = useAttention(sessionId);
	const numLayers = topology?.blocks?.length || 32;
	const numHeads = 32;
	const matrixData = (0, import_react.useMemo)(() => {
		if (!attentions) return null;
		return attentions.find((a) => a.layer === layer && a.head === head)?.matrix || null;
	}, [
		attentions,
		layer,
		head
	]);
	const max = matrixData ? Math.max(...matrixData.flat()) : 0;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
		title: "Attention Heatmap",
		subtitle: `Layer ${layer} · Head ${head}`,
		className: "h-full",
		actions: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "flex gap-2",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Select, {
				value: String(layer),
				onValueChange: (v) => setLayer(+v),
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectTrigger, {
					className: "h-7 w-20 text-xs",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectValue, {})
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectContent, {
					className: "max-h-60",
					children: Array.from({ length: numLayers }).map((_, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SelectItem, {
						value: String(i),
						children: ["L", i]
					}, i))
				})]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Select, {
				value: String(head),
				onValueChange: (v) => setHead(+v),
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectTrigger, {
					className: "h-7 w-20 text-xs",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectValue, {})
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectContent, {
					className: "max-h-60",
					children: Array.from({ length: numHeads }).map((_, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SelectItem, {
						value: String(i),
						children: ["H", i]
					}, i))
				})]
			})]
		}),
		children: [
			isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "p-8 text-center text-sm text-muted-foreground",
				children: "Loading attention matrices..."
			}),
			isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "p-8 text-center text-sm text-destructive",
				children: "Error loading attention data."
			}),
			!isLoading && !isError && !matrixData && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "p-8 text-center text-sm text-muted-foreground",
				children: [
					"No attention data available for L",
					layer,
					" H",
					head,
					"."
				]
			}),
			!isLoading && !isError && matrixData && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "grid gap-px",
				style: { gridTemplateColumns: `repeat(${matrixData.length}, minmax(0, 1fr))` },
				children: matrixData.map((row, i) => row.map((v, j) => {
					const intensity = max > 0 ? v / max : 0;
					return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						title: `q${i} → k${j}: ${v.toFixed(3)}`,
						className: "aspect-square rounded-[2px]",
						style: { backgroundColor: `color-mix(in oklab, var(--color-primary) ${Math.round(intensity * 100)}%, var(--color-secondary))` }
					}, `${i}-${j}`);
				}))
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mt-3 flex items-center justify-between text-[10px] text-muted-foreground",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "font-mono",
					children: "queries → keys"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex items-center gap-1",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "low" }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "h-2 w-24 rounded-full",
							style: { background: "linear-gradient(90deg, var(--color-secondary), var(--color-primary))" }
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "high" })
					]
				})]
			})] })
		]
	});
}
function RuntimeMetrics({ sessionId }) {
	const { data, isLoading, isError } = useMetrics(sessionId);
	const latestMetric = data && data.length > 0 ? data[0] : null;
	const items = [
		{
			label: "Latency",
			value: latestMetric ? `${latestMetric.dur_ms} ms` : "-",
			accent: "text-primary"
		},
		{
			label: "Throughput",
			value: latestMetric ? `- tok/s` : "-",
			accent: "text-[color:var(--color-info)]"
		},
		{
			label: "Shape",
			value: latestMetric?.shape || "-",
			mono: true
		},
		{
			label: "dtype",
			value: latestMetric?.dtype || "-",
			mono: true
		},
		{
			label: "Device",
			value: latestMetric?.device || "-",
			mono: true
		}
	];
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
		title: "Runtime Metrics",
		subtitle: isLoading ? "Loading..." : "Forward pass · current",
		className: "h-full",
		children: isError ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "p-4 text-center text-sm text-destructive",
			children: "Error loading runtime metrics."
		}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)("dl", {
			className: "grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5",
			children: items.map((it) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "rounded-md border border-border bg-secondary/40 px-3 py-2.5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("dt", {
					className: "text-[10px] uppercase tracking-wider text-muted-foreground",
					children: it.label
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("dd", {
					className: `mt-1 truncate text-sm font-semibold ${it.mono ? "font-mono" : ""} ${it.accent ?? ""}`,
					children: isLoading ? "..." : it.value
				})]
			}, it.label))
		})
	});
}
function ActivationStatistics({ sessionId }) {
	const { data, isLoading, isError } = useActivations(sessionId);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
		title: "Activation Statistics",
		subtitle: "Per-layer aggregate",
		className: "h-full",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "h-56",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "Loading activations..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-destructive",
					children: "Error loading activations."
				}),
				!isLoading && !isError && (!data || data.length === 0) && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "No activation data available."
				}),
				!isLoading && !isError && data && data.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ResponsiveContainer, {
					width: "100%",
					height: "100%",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(BarChart, {
						data,
						margin: {
							left: -16,
							right: 8,
							top: 8,
							bottom: 0
						},
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(XAxis, {
								dataKey: "layer",
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								},
								axisLine: false,
								tickLine: false
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(YAxis, {
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								},
								axisLine: false,
								tickLine: false
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Tooltip, { contentStyle: {
								background: "var(--color-popover)",
								border: "1px solid var(--color-border)",
								borderRadius: 8,
								fontSize: 12
							} }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Bar, {
								dataKey: "variance",
								fill: "var(--color-primary)",
								radius: [
									2,
									2,
									0,
									0
								]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Bar, {
								dataKey: "sparsity",
								fill: "var(--color-info)",
								radius: [
									2,
									2,
									0,
									0
								]
							})
						]
					})
				})
			]
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "mt-2 flex items-center justify-center gap-4 text-[11px] text-muted-foreground",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
				className: "flex items-center gap-1.5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "h-2 w-2 rounded-sm bg-primary" }), "variance"]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
				className: "flex items-center gap-1.5",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "h-2 w-2 rounded-sm bg-[color:var(--color-info)]" }), "sparsity"]
			})]
		})]
	});
}
var ICON = {
	info: Info,
	warn: TriangleAlert,
	error: CircleX
};
function AnomalyLedger({ sessionId }) {
	const { data, isLoading, isError } = useAnomalies(sessionId);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
		title: "Anomaly Ledger",
		subtitle: data ? `${data.length} events` : "Waiting for events",
		className: "h-full",
		contentClassName: "p-0",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("ul", {
			className: "max-h-72 divide-y divide-border overflow-auto",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", {
					className: "p-4 text-center text-sm text-muted-foreground",
					children: "Loading anomalies..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", {
					className: "p-4 text-center text-sm text-destructive",
					children: "Error loading anomalies."
				}),
				!isLoading && !isError && (!data || data.length === 0) && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("li", {
					className: "p-4 text-center text-sm text-muted-foreground",
					children: "No anomalies detected."
				}),
				!isLoading && !isError && data?.map((a) => {
					return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex items-start gap-3 px-4 py-3",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ICON[a.severity] || Info, { className: cn("mt-0.5 h-4 w-4 shrink-0", a.severity === "info" && "text-[color:var(--color-info)]", a.severity === "warn" && "text-[color:var(--color-warning)]", a.severity === "error" && "text-destructive") }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "min-w-0 flex-1",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "truncate text-sm text-foreground",
								children: a.message
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", {
								className: "mt-0.5 font-mono text-[10px] text-muted-foreground",
								children: [
									"layer ",
									a.layer,
									" · ",
									new Date(a.t).toLocaleTimeString()
								]
							})]
						})]
					}, a.id);
				})
			]
		})
	});
}
function MemoryMonitor({ sessionId }) {
	const { data, isLoading, isError } = useMemory(sessionId);
	const latest = data && data.length > 0 ? data[data.length - 1] : {
		gpu: 0,
		cpu: 0
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
		title: "Memory Monitor",
		subtitle: `GPU ${latest.gpu.toFixed(2)} GB · CPU ${latest.cpu.toFixed(2)} GB`,
		className: "h-full",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "h-48",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "Loading memory profile..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-destructive",
					children: "Error loading memory."
				}),
				!isLoading && !isError && (!data || data.length === 0) && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "No memory data available."
				}),
				!isLoading && !isError && data && data.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ResponsiveContainer, {
					width: "100%",
					height: "100%",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(AreaChart, {
						data,
						margin: {
							left: -16,
							right: 8,
							top: 8,
							bottom: 0
						},
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("defs", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("linearGradient", {
								id: "gpuGrad",
								x1: "0",
								x2: "0",
								y1: "0",
								y2: "1",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("stop", {
									offset: "0%",
									stopColor: "var(--color-primary)",
									stopOpacity: .6
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("stop", {
									offset: "100%",
									stopColor: "var(--color-primary)",
									stopOpacity: 0
								})]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("linearGradient", {
								id: "cpuGrad",
								x1: "0",
								x2: "0",
								y1: "0",
								y2: "1",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("stop", {
									offset: "0%",
									stopColor: "var(--color-info)",
									stopOpacity: .5
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("stop", {
									offset: "100%",
									stopColor: "var(--color-info)",
									stopOpacity: 0
								})]
							})] }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(XAxis, {
								dataKey: "t",
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								},
								axisLine: false,
								tickLine: false
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(YAxis, {
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								},
								axisLine: false,
								tickLine: false
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Tooltip, { contentStyle: {
								background: "var(--color-popover)",
								border: "1px solid var(--color-border)",
								borderRadius: 8,
								fontSize: 12
							} }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Area, {
								type: "monotone",
								dataKey: "gpu",
								stroke: "var(--color-primary)",
								fill: "url(#gpuGrad)",
								strokeWidth: 2
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Area, {
								type: "monotone",
								dataKey: "cpu",
								stroke: "var(--color-info)",
								fill: "url(#cpuGrad)",
								strokeWidth: 2
							})
						]
					})
				})
			]
		})
	});
}
function TokenTimeline({ sessionId }) {
	const { data, isLoading, isError } = useTokens(sessionId);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
		title: "Token Timeline",
		subtitle: data ? `${data.length} tokens generated` : "Waiting for tokens",
		className: "h-full",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "h-40",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "Loading tokens..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-destructive",
					children: "Error loading tokens."
				}),
				!isLoading && !isError && (!data || data.length === 0) && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "No token data available."
				}),
				!isLoading && !isError && data && data.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ResponsiveContainer, {
					width: "100%",
					height: "100%",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(LineChart, {
						data,
						margin: {
							left: -16,
							right: 8,
							top: 8,
							bottom: 0
						},
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(XAxis, {
								dataKey: "idx",
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								},
								axisLine: false,
								tickLine: false
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(YAxis, {
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								},
								axisLine: false,
								tickLine: false
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Tooltip, {
								contentStyle: {
									background: "var(--color-popover)",
									border: "1px solid var(--color-border)",
									borderRadius: 8,
									fontSize: 12
								},
								formatter: (v, _n, p) => [`${v} ms`, `"${p.payload.token}"`]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Line, {
								type: "monotone",
								dataKey: "ms",
								stroke: "var(--color-primary)",
								strokeWidth: 2,
								dot: {
									r: 3,
									fill: "var(--color-primary)"
								}
							})
						]
					})
				})
			]
		}), !isLoading && !isError && data && data.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			className: "mt-3 flex flex-wrap gap-1 font-mono text-xs",
			children: data.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
				className: "rounded border border-border bg-secondary/60 px-1.5 py-0.5 text-foreground",
				title: `${t.ms}ms`,
				children: t.token.trim() || "·"
			}, t.idx))
		})]
	});
}
var Tabs = Root2;
var TabsList = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(List, {
	ref,
	className: cn("inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground", className),
	...props
}));
TabsList.displayName = List.displayName;
var TabsTrigger = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Trigger, {
	ref,
	className: cn("inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background cursor-pointer transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow", className),
	...props
}));
TabsTrigger.displayName = Trigger.displayName;
var TabsContent = import_react.forwardRef(({ className, ...props }, ref) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Content, {
	ref,
	className: cn("mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2", className),
	...props
}));
TabsContent.displayName = Content.displayName;
function LayerRanking({ sessionId }) {
	const [sort, setSort] = (0, import_react.useState)("latency_ms");
	const { data: metrics, isLoading, isError } = useMetrics(sessionId);
	const data = (0, import_react.useMemo)(() => {
		if (!metrics) return [];
		const layerMap = {};
		metrics.forEach((m) => {
			if (!layerMap[m.layer]) layerMap[m.layer] = {
				latency_ms: 0,
				mem_mb: 0
			};
			layerMap[m.layer].latency_ms += m.dur_ms;
			layerMap[m.layer].mem_mb += 0;
		});
		return Object.entries(layerMap).map(([layer, stats]) => ({
			layer: parseInt(layer),
			latency_ms: stats.latency_ms,
			mem_mb: stats.mem_mb
		})).sort((a, b) => b[sort] - a[sort]).slice(0, 10);
	}, [metrics, sort]);
	const max = data.length > 0 ? Math.max(...data.map((d) => d[sort])) : 0;
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Panel, {
		title: "Layer Ranking",
		subtitle: "Top 10 layers",
		className: "h-full",
		actions: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Tabs, {
			value: sort,
			onValueChange: (v) => setSort(v),
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(TabsList, {
				className: "h-7",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(TabsTrigger, {
					value: "latency_ms",
					className: "h-5 px-2 text-[11px]",
					children: "Slowest"
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(TabsTrigger, {
					value: "mem_mb",
					className: "h-5 px-2 text-[11px]",
					children: "Heaviest"
				})]
			})
		}),
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "h-full min-h-32",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "Loading layer ranking..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-destructive",
					children: "Error loading ranking."
				}),
				!isLoading && !isError && data.length === 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "No layer data available."
				}),
				!isLoading && !isError && data.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("ul", {
					className: "space-y-1.5",
					children: data.map((d) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("li", {
						className: "flex items-center gap-3",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
								className: "w-12 shrink-0 font-mono text-xs text-muted-foreground",
								children: ["L", d.layer]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "relative h-5 flex-1 overflow-hidden rounded bg-secondary/60",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
									className: "h-full rounded bg-gradient-to-r from-primary/80 to-[color:var(--color-info)]/80",
									style: { width: max > 0 ? `${d[sort] / max * 100}%` : "0%" }
								})
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
								className: "w-20 shrink-0 text-right font-mono text-xs text-foreground",
								children: [
									d[sort].toFixed(2),
									" ",
									sort === "latency_ms" ? "ms" : "MB"
								]
							})
						]
					}, d.layer))
				})
			]
		})
	});
}
function HeadComparison({ sessionId }) {
	const [layer, setLayer] = (0, import_react.useState)(0);
	const { data: topology } = useTopology(sessionId);
	const { data: attentions, isLoading, isError } = useAttention(sessionId);
	const numLayers = topology?.blocks?.length || 32;
	const stats = (0, import_react.useMemo)(() => {
		if (!attentions) return [];
		return attentions.filter((a) => a.layer === layer).map((a) => {
			const flat = a.matrix.flat();
			const maxAttn = Math.max(...flat);
			const entropy = flat.reduce((acc, val) => acc - (val > 0 ? val * Math.log(val) : 0), 0);
			const sparsity = flat.filter((v) => v < .01).length / flat.length;
			return {
				head: a.head,
				entropy: entropy || 0,
				max_attn: maxAttn || 0,
				sparsity: sparsity || 0
			};
		});
	}, [attentions, layer]);
	const sampled = (0, import_react.useMemo)(() => {
		if (!stats.length) return [];
		const step = Math.max(1, Math.floor(stats.length / 8));
		return stats.filter((_, i) => i % step === 0).slice(0, 8);
	}, [stats]);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Panel, {
		title: "Head Comparison",
		subtitle: `Layer ${layer}`,
		className: "h-full",
		actions: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Select, {
			value: String(layer),
			onValueChange: (v) => setLayer(+v),
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectTrigger, {
				className: "h-7 w-20 text-xs",
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectValue, {})
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(SelectContent, {
				className: "max-h-60",
				children: Array.from({ length: numLayers }).map((_, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(SelectItem, {
					value: String(i),
					children: ["L", i]
				}, i))
			})]
		}),
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "h-48",
			children: [
				isLoading && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "Loading head stats..."
				}),
				isError && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-destructive",
					children: "Error loading head stats."
				}),
				!isLoading && !isError && sampled.length === 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex h-full items-center justify-center text-sm text-muted-foreground",
					children: "No attention data available."
				}),
				!isLoading && !isError && sampled.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ResponsiveContainer, {
					width: "100%",
					height: "100%",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(RadarChart, {
						data: sampled.map((s) => ({
							head: `H${s.head}`,
							entropy: s.entropy,
							max: s.max_attn * 3,
							sparsity: s.sparsity * 3
						})),
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(PolarGrid, { stroke: "var(--color-border)" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(PolarAngleAxis, {
								dataKey: "head",
								tick: {
									fill: "var(--color-muted-foreground)",
									fontSize: 10
								}
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Tooltip, { contentStyle: {
								background: "var(--color-popover)",
								border: "1px solid var(--color-border)",
								borderRadius: 8,
								fontSize: 12
							} }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Radar, {
								dataKey: "entropy",
								stroke: "var(--color-primary)",
								fill: "var(--color-primary)",
								fillOpacity: .3
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Radar, {
								dataKey: "max",
								stroke: "var(--color-info)",
								fill: "var(--color-info)",
								fillOpacity: .2
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Radar, {
								dataKey: "sparsity",
								stroke: "var(--color-warning)",
								fill: "var(--color-warning)",
								fillOpacity: .2
							})
						]
					})
				})
			]
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "mt-2 flex flex-wrap items-center justify-center gap-3 text-[11px] text-muted-foreground",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
					className: "flex items-center gap-1.5",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "h-2 w-2 rounded-sm bg-primary" }), "entropy"]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
					className: "flex items-center gap-1.5",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "h-2 w-2 rounded-sm bg-[color:var(--color-info)]" }), "max attn"]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
					className: "flex items-center gap-1.5",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "h-2 w-2 rounded-sm bg-[color:var(--color-warning)]" }), "sparsity"]
				})
			]
		})]
	});
}
function DashboardPage() {
	useNavigate({ from: "/dashboard" });
	const sessionId = useCurrentSessionId();
	if (!sessionId) return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "grid h-screen place-items-center text-center",
		children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", {
				className: "text-lg font-semibold",
				children: "No active session"
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
				className: "text-sm text-muted-foreground mb-4",
				children: "Please start a tracing session first."
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
				to: "/",
				className: "text-primary hover:underline",
				children: "Go back home"
			})
		] })
	});
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "min-h-screen",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("header", {
			className: "sticky top-0 z-20 border-b border-border bg-background/80 backdrop-blur",
			children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "grid grid-cols-[minmax(0,1fr)_auto] items-center gap-4 px-4 py-3 sm:flex sm:flex-wrap sm:justify-between sm:px-6",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "flex min-w-0 items-center gap-3",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
							to: "/",
							className: "grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-border bg-secondary text-muted-foreground transition-colors hover:text-foreground",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, { className: "h-4 w-4" })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "grid h-9 w-9 shrink-0 place-items-center rounded-lg border border-primary/40 bg-primary/10",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Activity, { className: "h-4 w-4 text-primary" })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "min-w-0",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", {
								className: "truncate text-sm font-semibold sm:text-base",
								children: ["LLM ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "text-gradient",
									children: "Inspector"
								})]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "truncate font-mono text-[11px] text-muted-foreground",
								children: sessionId
							})]
						})
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "flex shrink-0 items-center gap-3 text-xs",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
						className: "flex items-center gap-1.5 rounded-full border border-[color:var(--color-success)]/40 bg-[color:var(--color-success)]/10 px-2.5 py-1 text-[color:var(--color-success)]",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Circle, { className: "h-2 w-2 fill-current" }), "Live Connected"]
					})
				})]
			})
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("main", {
			className: "p-4 sm:p-6",
			children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mb-4",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(RuntimeMetrics, { sessionId })
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "grid gap-4 lg:grid-cols-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ModelTopology, { sessionId }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "lg:col-span-2",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(LiveExecutionStream, { sessionId })
					})]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-4 grid gap-4 lg:grid-cols-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(AttentionHeatmap, { sessionId }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(HeadComparison, { sessionId })]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-4 grid gap-4 lg:grid-cols-2",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(MemoryMonitor, { sessionId }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ActivationStatistics, { sessionId })]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mt-4 grid gap-4 lg:grid-cols-3",
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "lg:col-span-2",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(TokenTimeline, { sessionId })
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(AnomalyLedger, { sessionId })]
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "mt-4",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(LayerRanking, { sessionId })
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("footer", {
					className: "mt-8 text-center text-[11px] text-muted-foreground",
					children: "LLM Inspector · Backend Source of Truth · WebSockets ready"
				})
			]
		})]
	});
}
//#endregion
export { DashboardPage as component };
