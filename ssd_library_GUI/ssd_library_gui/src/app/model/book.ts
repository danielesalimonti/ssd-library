
export class Book {

  constructor(
    public isbn: string,
    public author: string,
    public title: string,
    public preview: string,
    public description: string,
    public publishedDate: Date,
    public numPages: number,
  ) {
  }
}
