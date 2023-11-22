export interface Email {
    pk: number;
    from: string;
    recipients: [string];
    subject: string;
    body: string;
    timestamp: Date;
    read: boolean;
    archived: boolean;
}