import React, {useState} from "react";
import {ParameterRule} from "@/app/api/model-provider/model";

type Props = {
  params: ParameterRule[];
  language?: "zh_Hans" | "en_US";
  onChange?: (form: Record<string, any>) => void;
};

export default function DynamicForm({params, language = "zh_Hans", onChange}: Props) {
  const [formData, setFormData] = useState<Record<string, any>>(
    Object.fromEntries((params ?? []).map(p => [p.name, p.default ?? ""]))
  );

  const handleChange = (name: string, value: any) => {
    const updated = {...formData, [name]: value};
    setFormData(updated);
    onChange?.(updated);
  };

  const renderInput = (param: ParameterRule) => {
    const value = formData[param.name]??(param.default ?? 0);
    const precision = param.precision ?? 2;
    const step = Math.pow(10, -precision);

    if (param.options && param.options.length > 0) {
      return (
        <select
          value={value}
          onChange={e => handleChange(param.name, e.target.value)}
          className="border rounded px-2 py-1 w-full"
        >
          {param.options.map(opt => (
            <option key={opt ?? opt} value={opt ?? opt}>
              {opt}
            </option>
          ))}
        </select>
      );
    }

    if (param.type === "int" || param.type === "float") {
      return (
        <div className="flex flex-row items-center gap-4 w-full">
          <input
            type="range"
            min={param.min ?? 0}
            max={param.max ?? 100}
            step={step}
            value={value}
            onChange={e =>
              handleChange(param.name, param.type === "int" ? parseInt(e.target.value) : parseFloat(e.target.value))
            }
            className="flex-1 h-4"
          />
          <input
            type="number"
            value={value}
            step={step}
            min={param.min ?? undefined}
            max={param.max ?? undefined}
            onChange={e =>
              handleChange(param.name, param.type === "int" ? parseInt(e.target.value) : parseFloat(e.target.value))
            }
            className="w-16 border rounded text-sm px-1 py-0.5" // 缩小尺寸
          />
        </div>
      );
    }

    return (
      <input
        type="text"
        value={value}
        onChange={e => handleChange(param.name, e.target.value)}
        className="border rounded w-32 text-sm px-1 py-0.5"
      />
    );
  };

  return (
    <div style={{height: "340px",width:"420px", overflowY: "auto", boxSizing: "border-box"}}>
      <form className="space-y-3">
        {params?.map(param => {
          const label = param.label?.[language] ?? param.name;
          const help = param.help?.[language] ?? "";

          return (
            <div key={param.name} className="flex flex-row items-center gap-3">
              {/* label 和 tooltip 在 group 内 */}
              <div className="relative group w-32 shrink-0">
                <div className="font-medium text-sm cursor-help text-gray-400">
                  {label} {param.required ? "*" : ""}
                </div>
                {help && (
                  <div className="absolute left-full top-1/2 -translate-y-1/2 ml-2
                  bg-gray-700 text-white text-xs px-2 py-1 rounded
                  opacity-0 group-hover:opacity-100
                  whitespace-pre-wrap z-10 transition-opacity
                  w-52 break-words pointer-events-none">
                    {help}
                  </div>
                )}
              </div>

              {/* 控件 */}
              <div className="flex-1">{renderInput(param)}</div>
            </div>

          );
        })}
      </form>
    </div>
  );
}
