export type InteractionMode = "interactive" | "autonomous" | "delegated" | "workflow";
export type PermissionLevel = "read-only" | "scoped-write" | "privileged";

export interface ContextSurface {
  readonly id: string;
  readonly description: string;
  readonly sensitivity: "public" | "internal" | "sensitive";
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
  };
  readonly approvalFlow: {
    readonly requiredFor: readonly string[];
    readonly approverRoles: readonly string[];
  };
  readonly handoffBoundaries: readonly string[];
}
