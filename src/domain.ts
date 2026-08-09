export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };
export type EvidencePayload = Readonly<Record<string, JsonValue>>;

export type ValidationSeverity = "error" | "warning";

export interface ValidationFinding {
  readonly code: string;
  readonly severity: ValidationSeverity;
  readonly path: string;
  readonly message: string;
}

export interface ValidationResult {
  readonly valid: boolean;
  readonly findings: readonly ValidationFinding[];
}

export function validationResult(findings: readonly ValidationFinding[]): ValidationResult {
  return {
    valid: findings.every((finding) => finding.severity !== "error"),
    findings,
  };
}
