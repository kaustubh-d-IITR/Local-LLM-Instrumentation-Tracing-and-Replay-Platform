import { i as __toESM } from "../_runtime.mjs";
import { u as require_react } from "../_libs/@floating-ui/react-dom+[...].mjs";
import { i as Slot, s as require_jsx_runtime } from "../_libs/@radix-ui/react-arrow+[...].mjs";
import { t as cva } from "../_libs/class-variance-authority+clsx.mjs";
import { a as useCreateSession, t as cn } from "./utils-C2sR9Z8l.mjs";
import { M as useNavigate } from "../_libs/@tanstack/react-router+[...].mjs";
import { c as Activity, n as Cpu, u as Sparkles } from "../_libs/lucide-react.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-cxa7wDL9.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var buttonVariants = cva("inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium cursor-pointer transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0", {
	variants: {
		variant: {
			default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
			destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
			outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
			secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
			ghost: "hover:bg-accent hover:text-accent-foreground",
			link: "text-primary underline-offset-4 hover:underline"
		},
		size: {
			default: "h-9 px-4 py-2",
			sm: "h-8 rounded-md px-3 text-xs",
			lg: "h-10 rounded-md px-8",
			icon: "h-9 w-9"
		}
	},
	defaultVariants: {
		variant: "default",
		size: "default"
	}
});
var Button = import_react.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(asChild ? Slot : "button", {
		className: cn(buttonVariants({
			variant,
			size,
			className
		})),
		ref,
		...props
	});
});
Button.displayName = "Button";
var Textarea = import_react.forwardRef(({ className, ...props }, ref) => {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("textarea", {
		className: cn("flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-base shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm", className),
		ref,
		...props
	});
});
Textarea.displayName = "Textarea";
var MODELS = [
	{
		id: "llama",
		name: "Llama 3.1 8B",
		layers: 32,
		heads: 32,
		hidden: 4096,
		params: "8B"
	},
	{
		id: "gemma",
		name: "Gemma 2 9B",
		layers: 42,
		heads: 16,
		hidden: 3584,
		params: "9B"
	},
	{
		id: "qwen",
		name: "Qwen 2.5 7B",
		layers: 28,
		heads: 28,
		hidden: 3584,
		params: "7B"
	},
	{
		id: "mistral",
		name: "Mistral 7B",
		layers: 32,
		heads: 32,
		hidden: 4096,
		params: "7B"
	}
];
function SessionCreatePage() {
	const navigate = useNavigate();
	const [model, setModel] = (0, import_react.useState)("llama");
	const [prompt, setPrompt] = (0, import_react.useState)("Explain how multi-head attention works in a transformer block.");
	const createSessionMutation = useCreateSession();
	const submit = () => {
		if (!prompt.trim()) return;
		createSessionMutation.mutate({
			model_name: model,
			prompt: prompt.trim()
		}, { onSuccess: () => {
			navigate({ to: "/dashboard" });
		} });
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("main", {
		className: "relative min-h-screen overflow-hidden",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			"aria-hidden": true,
			className: "pointer-events-none absolute inset-0 opacity-40",
			style: { backgroundImage: "radial-gradient(circle at 20% 0%, color-mix(in oklab, var(--color-primary) 25%, transparent), transparent 50%), radial-gradient(circle at 80% 100%, color-mix(in oklab, var(--color-info) 25%, transparent), transparent 50%)" }
		}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
			className: "relative mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center px-6 py-12",
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mb-10 flex items-center gap-3",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
					className: "grid h-10 w-10 place-items-center rounded-xl border border-primary/40 bg-primary/10",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Activity, { className: "h-5 w-5 text-primary" })
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", {
					className: "text-2xl font-bold tracking-tight",
					children: ["LLM ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
						className: "text-gradient",
						children: "Inspector"
					})]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
					className: "text-xs text-muted-foreground",
					children: "Local LLM instrumentation · tracing · replay"
				})] })]
			}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("section", {
				className: "panel p-6 sm:p-8",
				children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mb-6",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
							className: "mb-3 block text-xs font-medium uppercase tracking-wider text-muted-foreground",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Cpu, { className: "mr-1.5 -mt-0.5 inline h-3.5 w-3.5" }), "Select model"]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "grid grid-cols-2 gap-2 sm:grid-cols-4",
							children: MODELS.map((m) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("button", {
								onClick: () => setModel(m.id),
								className: cn("group flex flex-col items-start gap-1 rounded-lg border px-3 py-3 text-left transition-all", model === m.id ? "border-primary bg-primary/10 glow-primary" : "border-border bg-secondary/40 hover:border-primary/40 hover:bg-secondary"),
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "text-sm font-semibold text-foreground",
									children: m.name.split(" ")[0]
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
									className: "font-mono text-[10px] text-muted-foreground",
									children: [
										m.params,
										" · ",
										m.layers,
										"L · ",
										m.heads,
										"H"
									]
								})]
							}, m.id))
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mb-6",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
							htmlFor: "prompt",
							className: "mb-3 block text-xs font-medium uppercase tracking-wider text-muted-foreground",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Sparkles, { className: "mr-1.5 -mt-0.5 inline h-3.5 w-3.5" }), "Prompt"]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Textarea, {
							id: "prompt",
							value: prompt,
							onChange: (e) => setPrompt(e.target.value),
							rows: 6,
							className: "resize-none border-border bg-secondary/40 font-mono text-sm focus-visible:ring-primary",
							placeholder: "Enter the prompt to trace…"
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "flex items-center justify-between gap-3",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
							className: "text-xs text-muted-foreground",
							children: "Connected to backend source of truth."
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							onClick: submit,
							disabled: createSessionMutation.isPending || !prompt.trim(),
							className: "gap-2",
							children: [createSessionMutation.isPending ? "Starting…" : "Start session", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
								"aria-hidden": true,
								children: "→"
							})]
						})]
					})
				]
			})]
		})]
	});
}
//#endregion
export { SessionCreatePage as component };
