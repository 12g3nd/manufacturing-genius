-- Give native MathML a real HTML scroll container on narrow screens.
function Math(el)
  local kind = el.mathtype == "DisplayMath" and "math-block" or "math-inline"
  return pandoc.Span({el}, pandoc.Attr("", {"math-wrap", kind}))
end
