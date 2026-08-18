export type InteractionMode = "interactive" | "autonomous" | "delegated" | "workflow";
export type PermissionLevel = "read-only" | "scoped-write" | "privileged";

export interface ContextSurface {
  readonly id: string;
  readonly description: string;
  readonly sensitivity: "public" | "internal" | "sensitive";
  readonly projection?: LasmProjectionReferences;
}

export interface HandoffBoundary {
  readonly id: string;
  readonly description: string;
  readonly projection?: LasmProjectionReferences;
}

export interface HarnessDescriptor {
  readonly id: string;
  readonly name: string;
  readonly purpose: string;
  readonly interactionMode: InteractionMode;
  readonly contextSurfaces: readonly ContextSurface[];
  readonly affordances: readonly string[];
  readonly permissionModel: {
    readonly defaultLevel: PermissionLevel;
    readonly scopedPermissions: readonly string[];
    readonly projection?: LasmProjectionReferences;
  };
  readonly approvalFlow: {
    readonly requiredFor: readonly string[];
    readonly approverRoles: readonly string[];
    readonly projection?: LasmProjectionReferences;
  };
  readonly handoffBoundaries: readonly HandoffBoundary[];
  readonly projection?: LasmProjectionReferences;
}
import type { LasmProjectionReferences } from "./lasm.js";
