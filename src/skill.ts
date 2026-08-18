export interface SkillReference {
  readonly kind: "instruction" | "reference" | "script" | "asset";
  readonly name: string;
}

export interface SkillDescriptor {
  readonly id: string;
  readonly name: string;
  readonly purpose: string;
  readonly applicability: readonly string[];
  readonly capabilities: readonly string[];
  readonly references?: readonly SkillReference[];
  readonly projection?: LasmProjectionReferences;
}
import type { LasmProjectionReferences } from "./lasm.js";
