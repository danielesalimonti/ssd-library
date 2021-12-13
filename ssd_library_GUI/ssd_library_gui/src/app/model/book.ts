
export class Book {

  constructor(
    public ISBN: string,
    public author: string,
    public title: string,
    public preview: string,
    public text: string,
    public published_date: Date,
    public num_pages: number,
  ) {
  }
}
