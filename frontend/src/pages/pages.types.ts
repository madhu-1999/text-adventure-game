export const FormActionType = {
  RESET: "RESET_FORM",
  VALIDATE: "VALIDATE_FORM",
  UPDATE: "UPDATE_FIELD",
} as const;

type FormActionType = (typeof FormActionType)[keyof typeof FormActionType];

interface ResetAction {
  type: typeof FormActionType.RESET;
}

interface ValidateAction {
  type: typeof FormActionType.VALIDATE;
}

interface UpdateAction {
  type: typeof FormActionType.UPDATE;
  payload: {
    field: string;
    value: string;
  };
}
export type FormAction = ResetAction | ValidateAction | UpdateAction;
