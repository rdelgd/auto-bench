export type McpRisk = "low" | "moderate" | "high";

export interface McpPrimitiveDescriptor {
  readonly id: string;
  readonly name: string;
  readonly purpose: string;
  readonly risk: McpRisk;
  readonly requiredPermission?: string;
}

export interface McpSurfaceDescriptor {
  readonly id: string;
  readonly name: string;
  readonly purpose: string;
  readonly tools: readonly McpPrimitiveDescriptor[];
  readonly resources: readonly McpPrimitiveDescriptor[];
  readonly prompts: readonly McpPrimitiveDescriptor[];
}

export function mcpPrimitives(surface: McpSurfaceDescriptor): readonly McpPrimitiveDescriptor[] {
  return [...surface.tools, ...surface.resources, ...surface.prompts];
}
