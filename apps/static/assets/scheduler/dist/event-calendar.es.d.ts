declare type TDataBlock = {
    in: string[];
    out: string[];
    exec: any;
    length?: number;
};
declare type TDataConfig = TDataBlock[];
declare type TID$1 = number | string;
declare type TDispatch$1<T> = <A extends keyof T>(action: A, data: T[A]) => void;
interface DataHash {
    [key: string]: any;
}
interface IWritable<T> {
    subscribe: (fn: (v: T) => any) => any;
    update: (fn: (v: T) => any) => any;
    set: (val: T) => any;
}
declare type TWritableCreator = (val: any) => IWritable<typeof val>;

declare type TState<Type> = {
    [Property in keyof Type]: IWritable<Type[Property]>;
};
declare class Store<T extends DataHash> {
    private _state;
    private _values;
    private _writable;
    constructor(writable: TWritableCreator);
    setState(data: Partial<T>): void;
    getState(): T;
    getReactive(): TState<T>;
    private _wrapWritable;
}

declare class EventBus<T> {
    private _handlers;
    protected _nextHandler: TDispatch$1<T>;
    constructor();
    on(name: string, handler: any): void;
    exec(name: string, ev: any): void;
    setNext(next: TDispatch$1<T>): void;
}

declare type TMethodsConfig = IDataMethodsConfig;
declare type TDispatch = <A extends keyof TMethodsConfig>(action: A, data: TMethodsConfig[A]) => void;
interface IDataConfig {
    events: IEventData[];
    selected: IEventData;
    mode: string;
    date: Date;
    sidebar: {
        show: boolean;
    } | false;
    editorShape?: TEditorShape[];
    calendars?: ICalendar[];
    config: ISchedulerConfig$1;
    colors?: IColorSchema[];
}
interface IBaseViewConfig {
    cellCss?: (date: Date) => string;
    template?: (event: IEventData) => string;
    dateTitle?: (currentDate: Date, bounds: [Date, Date]) => string;
    eventHeight?: number;
}
interface IReadonlyConfig {
    dragResize?: boolean;
    readonly?: boolean;
    dragMove?: boolean;
}
declare type IViewConfig = IWeekConfig | IMonthConfig | ITimelineConfig | IBaseViewConfig;
interface IViewItem {
    id: TID;
    label: string;
    layout: "day" | "week" | "month" | "year" | "agenda" | "timeline";
    config?: IViewConfig;
}
interface ISchedulerConfig$1 extends IReadonlyConfig {
    tableHeaderHeight?: number;
    autoSave?: boolean;
    dimPastEvents?: boolean;
    timeStep?: number;
    dragCreate?: boolean;
    eventInfoOnClick?: boolean;
    eventsOverlay?: boolean;
    eventHeight?: number;
    timeRange?: [number, number];
    editorOnDblClick?: boolean;
    createEventOnDblClick?: boolean;
    eventVerticalSpace?: number;
    defaultEventDuration?: number;
    viewControl?: "auto" | "toggle" | "dropdown" | "none";
    views?: IViewItem[];
    dateClick?: boolean | TID;
    editorValidation?: (event: IEventData) => string | false;
    dateTitle?: (date: Date, bounds: [Date, Date]) => string;
}
interface IData {
    events: IEventData[];
    selected: IEventData;
    selectedId: TID;
    popupInfo: boolean;
    edit: "add" | "update" | boolean;
    mode: string;
    date: Date;
    bounds: [Date, Date];
    viewSize: {
        width: number;
        height: number;
    };
    viewData: any[];
    viewModel: any;
    editorShape?: TEditorShape[];
    calendars?: ICalendar[];
    config: ISchedulerConfig$1;
    datepicker: TDatepickerConfig;
    sidebar: {
        show: boolean;
    } | false;
    colors: IColorSchema[];
    dateFnsLocale?: any;
}
interface IApi {
    exec: any;
    on: any;
    getState: any;
    getReactiveState: any;
    setNext: (ev: IEventBus) => void;
    getStores: () => {
        state: DataStore;
    };
    intercept: any;
}
interface IEventBus {
    exec(name: string, ev: any): void;
    setNext(next: TDispatch): void;
}
declare type IOption = {
    id: TID;
    label?: string;
    [key: string]: any;
};
declare type TCommonShape = {
    key: string | any;
    label?: string;
    id?: TID;
};
declare type ICommonConfig = {
    disabled?: boolean;
    placeholder?: string;
    [key: string]: any;
};
declare type TTextFieldShape = TCommonShape & {
    type: "text" | "textarea";
    config?: ICommonConfig & {
        readonly?: boolean;
        focus?: boolean;
        type?: string;
        inputStyle?: string;
    };
};
declare type TCheckboxShape = TCommonShape & {
    type: "checkbox";
    text?: string;
};
declare type TRecurringEvent = TCommonShape & {
    type: "recurring";
};
declare type TRadioShape = TCommonShape & {
    type: "radio";
    options: {
        id: TID;
        label?: string;
    }[];
};
declare type TComboFieldShape = TCommonShape & {
    type: "combo" | "select" | "multiselect";
    options?: IOption[];
    template?: (opt: IOption) => string;
    config?: ICommonConfig;
};
declare type TColorFieldShape = TCommonShape & {
    type: "color";
    colors?: string[];
    config?: ICommonConfig & {
        clear?: boolean;
    };
};
declare type TColorSchemaFieldShape = TCommonShape & {
    type: "colorSchema";
    colors?: IColorSchema[];
    config?: ICommonConfig & {
        clear?: boolean;
    };
};
declare type TDateFieldShape = TCommonShape & {
    type: "date";
    time?: boolean;
    config?: ICommonConfig;
};
declare type TFilesFieldShape = TCommonShape & {
    type: "files";
    uploadURL?: string;
    config?: IUploaderConfig;
};
interface IUploaderConfig {
    accept?: string;
    disabled?: boolean;
    multiple?: boolean;
    folder?: boolean;
}
declare type TEditorShape = TTextFieldShape | TComboFieldShape | TColorFieldShape | TDateFieldShape | TCheckboxShape | TRadioShape | TColorSchemaFieldShape | TRecurringEvent | TFilesFieldShape;
declare type TID = string | number;
interface IColorSchema {
    background?: string;
    border?: string;
    textColor?: string;
    colorpicker?: string;
}
interface IEventData extends IReadonlyConfig {
    start_date: Date;
    end_date: Date;
    id?: TID;
    type?: TID;
    text?: string;
    details?: string;
    allDay?: boolean;
    color?: IColorSchema;
    recurring?: boolean;
    STDATE?: Date;
    DTEND?: Date;
    RRULE?: string | IRRULEObject;
    EXDATE?: Date[];
    section?: TID;
    [key: string]: any;
}
interface ICalendar {
    id: TID;
    label: string;
    active: boolean;
    color?: IColorSchema;
    readonly?: boolean;
}
declare type TDatepickerConfig = {
    current: Date;
    markers: (d: Date) => string;
};
interface IRRULEObject {
    FREQ?: "DAILY" | "WEEKLY" | "MONTHLY" | "YEARLY";
    INTERVAL?: number;
    BYDAY?: string[];
    BYMONTH?: number;
    BYMONTHDAY?: number;
    BYSETPOS?: number;
    UNTIL?: Date;
    COUNT?: number;
    EXDATE?: Date[];
    weekDays?: IWeekDays;
    [key: string]: any;
}
declare type IWeekDays = {
    id: string;
    name: string;
    index: number;
    fullName: string;
}[];
interface IWeekConfig extends IBaseViewConfig {
    timeRange?: [number, number];
    timeStep?: number;
    eventsOverlay?: false;
    eventVerticalSpace?: number;
    eventHorizontalSpace?: string;
    columnPadding?: string;
    weekStartsOn?: number;
    /** @deprecated eventHorizontalSpace field instead */
    eventMargin?: string;
}
interface IMonthConfig extends IBaseViewConfig {
    weekStartsOn?: number;
    maxEventsPerCell?: number;
    eventVerticalSpace?: number;
}
interface ITimelineHeader {
    unit: string;
    format: string;
    step: number;
}
interface ITimelineConfig extends IBaseViewConfig {
    colsCount?: number;
    colsWidth?: number;
    minEventWidth?: number;
    eventVerticalSpace?: number;
    minSectionHeight?: number;
    sectionWidth?: number;
    getBounds?: (date: Date, config: ITimelineConfig) => [Date, Date];
    getNext?: (date: Date, config: ITimelineConfig) => Date;
    getPrev?: (date: Date, config: ITimelineConfig) => Date;
    step?: [number, "day" | "week" | "month" | "year" | "hour" | "minute"];
    header?: ITimelineHeader[];
    sections?: ISection[];
    key?: string;
    unassignedCol?: boolean;
}
interface ISection {
    id: TID;
    label?: string;
    [key: string]: any;
}

declare class DataStore extends Store<IData> {
    in: EventBus<TMethodsConfig>;
    private _router;
    private _registeredViews;
    private _uniqueId;
    constructor(w: TWritableCreator);
    init(state: Partial<IDataConfig>): void;
    setState(state: Partial<IData>, ctx?: TDataConfig): void;
    normalizeState(initData: Partial<IData>): {
        editorShape: any[];
        events: IEventData[];
        calendars: ICalendar[];
    };
    _checkId(id: TID$1): void;
}
interface IDataMethodsConfig {
    ["set-date"]: {
        value: Date;
    };
    ["set-mode"]: {
        value: string;
    };
    ["set-bound"]: {
        step: number;
    };
    ["add-event"]: {
        event: IEventData;
    };
    ["delete-event"]: {
        id: TID$1;
    };
    ["update-event"]: {
        event: IEventData;
        id: TID$1;
    };
    ["update-calendar"]: {
        calendar: ICalendar;
        id: TID$1;
    };
    ["add-calendar"]: {
        calendar: ICalendar;
    };
    ["delete-calendar"]: {
        id: TID$1;
    };
    ["toggle-sidebar"]: {
        show: boolean;
    } | null;
    ["select-event"]: {
        id: TID$1;
        popup?: boolean;
    };
    ["edit-event"]: {
        id?: TID$1;
        add?: IEventData | Record<string, never>;
    } | null;
    ["close-event-info"]: null;
}

declare const defaultColors: IColorSchema[];
declare const defaultCalendars: ICalendar[];
declare const defaultEditorShape: TEditorShape[];

declare const en: any;

declare const de: any;

declare const ru: any;

declare function uid(): string;

declare class Events {
    private _api;
    constructor(api: IApi);
    on<K extends keyof TMethodsConfig>(event: K, callback: (config: TMethodsConfig[K]) => any): void;
    exec<K extends keyof TMethodsConfig>(event: K, data: TMethodsConfig[K]): void;
}

declare type IEventTemplate = (event: IEventData, calendar: ICalendar) => string;
declare type ITheme = "willow" | "material" | "willowDark";
interface ISchedulerConfig extends Partial<IDataConfig> {
    locale?: typeof en;
    theme?: ITheme;
    templates?: {
        monthEvent?: IEventTemplate;
        weekEvent?: IEventTemplate;
        multievent?: IEventTemplate;
        popup?: IEventTemplate;
        header?: (date: Date, dateFormat: string) => string;
    };
}
declare class EventCalendar {
    api: IApi;
    events: Events;
    config: ISchedulerConfig;
    container: HTMLElement;
    private _widget;
    constructor(container: HTMLElement | string, config?: ISchedulerConfig);
    destructor(): void;
    setConfig(config: Partial<ISchedulerConfig>): void;
    parse(data: IEventData[] | {
        events: IEventData[];
        calendars: ICalendar[];
    }): void;
    serialize(): {
        events: IEventData[];
        calendars: ICalendar[];
    };
    addEvent(config: TMethodsConfig["add-event"]): void;
    deleteEvent(config: TMethodsConfig["delete-event"]): void;
    updateEvent(config: TMethodsConfig["update-event"]): void;
    updateCalendar(config: TMethodsConfig["update-calendar"]): void;
    addCalendar(config: TMethodsConfig["add-calendar"]): void;
    deleteCalendar(config: TMethodsConfig["delete-calendar"]): void;
    getCalendar(config: {
        id: TID;
    }): any;
    toggleSidebar(config?: TMethodsConfig["toggle-sidebar"]): void;
    setMode(config: TMethodsConfig["set-mode"]): void;
    setDate(config: TMethodsConfig["set-date"]): void;
    showEventInfo(config: {
        id: TID;
    }): void;
    hideEventInfo(): void;
    createEvent(config?: {
        event: IEventData;
    }): void;
    openEditor(config?: {
        id: TID;
    }): void;
    closeEditor(): void;
    getState(): any;
    getEvent(config: {
        id: TID;
    }): any;
    setLocale(locale: typeof en): void;
    setTheme(theme: ITheme): void;
    private _init;
    private _reset;
    private _storeConfig;
    private _configToProps;
}

declare class RestDataProvider extends EventBus<TMethodsConfig> {
    private _url;
    private _customHeaders;
    private _queue;
    constructor(url?: string);
    getIDResolver(): any;
    getEvents(): Promise<IEventData[]>;
    getCalendars(): Promise<IEventData[]>;
    setHeaders(headers: any): void;
    protected getHandlers(handlers: Partial<Record<keyof TMethodsConfig, any>>): Partial<Record<keyof TMethodsConfig, any>>;
    protected send<T>(url: string, method: string, data?: any, customHeaders?: any): Promise<T>;
    protected parseEvents(data: any[]): any[];
}

declare class RemoteEvents {
    protected _remote: any;
    protected _ready: Promise<any>;
    constructor(url: string, token: string);
    protected ready(): Promise<any>;
    protected on(name: string | any, handler?: any): void;
}

declare function remoteUpdates(api: any, resolver: any): any;

export { EventCalendar, RemoteEvents, RestDataProvider, de, defaultCalendars, defaultColors, defaultEditorShape, en, remoteUpdates, ru, uid };
