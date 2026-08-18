import type { EvidencePayload, JsonValue } from "./domain.js";

export interface OperationalStateField {
  readonly id: string;
  readonly conceptId: string;
  readonly value: JsonValue;
}

export interface OperationalState {
  readonly id: string;
  readonly assemblyId: string;
  readonly assemblyVersion: string;
  readonly fields: readonly OperationalStateField[];
}

export interface ActorObservation {
  readonly id: string;
  readonly actorId: string;
  readonly fieldIds: readonly string[];
  readonly observedValues: EvidencePayload;
}

export type TransitionDisposition = "permitted" | "prohibited";

export interface StateTransitionExpectation {
  readonly id: string;
  readonly description: string;
  readonly disposition: TransitionDisposition;
  readonly required: boolean;
  readonly eventId?: string;
  readonly fieldIds: readonly string[];
  readonly before?: EvidencePayload;
  readonly after?: EvidencePayload;
}

export type OutcomeDisposition = "acceptable" | "prohibited";

export interface OutcomeExpectation {
  readonly id: string;
  readonly description: string;
  readonly disposition: OutcomeDisposition;
  readonly required: boolean;
  readonly fieldIds: readonly string[];
}
