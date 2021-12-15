import {Component, OnDestroy, OnInit} from '@angular/core';
import {Book} from '../model/book';
import {Router} from '@angular/router';
import {BookService} from '../../services/book.service';
import {AuthService} from '../../services/auth.service';
import {ToastController} from '@ionic/angular';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {

  isLogged = false;
  loadingBooks = true;
  loadingMyBooks = true;
  books: Book[] = [];
  isMyBook: string[] = [];
  searchField: FormControl = new FormControl('');
  orderField: FormControl = new FormControl('');
  orderAscending = true;

  constructor(private router: Router,
              private bookService: BookService,
              private auth: AuthService,
              private toastController: ToastController,
              ) {
    this.isLogged = this.auth.isLogged();
  }

  ngOnInit() {
      this.bookService.getAllBooks().subscribe(
        (data) => {
          this.books = data;
          this.loadingBooks = false;

          this.updateButtons();
        },
        error => {
          if (error.status === 0) {
            error.error.detail = 'Lost Connection';
          }
          localStorage.setItem('error', JSON.stringify({status: error.status, message: error.error.detail}));
          this.router.navigateByUrl('/error-page', {replaceUrl: true})
        });
  }

  filter(books: Book[]): Book[]{
    return books.filter(b => this.searchField.value === ''
      || b.ISBN.includes(this.searchField.value)
      || b.title.toLowerCase().includes(this.searchField.value.toLowerCase())
      || b.author.toLowerCase().includes(this.searchField.value.toLowerCase()));
  }

  sort(books: Book[]): Book[]{
    return books.sort( (a, b) => {
      let c;
      switch(this.orderField.value){
        case 'ISBN': c = a.ISBN.localeCompare(b.ISBN); break;
        case 'Title': c = a.title.localeCompare(b.title); break;
        case 'Author': c = a.author.localeCompare(b.author); break;
        case 'PublishDate': c = a.published_date > b.published_date ? 1 : -1; break;
        default: return this.orderAscending ? 0 : -1;
      }
      return this.orderAscending ? c : -c;
    });
  }

  updateButtons(){
    if(this.isLogged) {
      this.bookService.getMyBooks().subscribe(
        (myBooks) => {
          this.isMyBook = [];
          myBooks.forEach((b) => {
            this.isMyBook.push(b.ISBN);
          });
          this.loadingMyBooks = false;
        },
        error => this.createToast(error));
    }else{
      this.loadingMyBooks = false;
    }
  }

  rent(isbn){
    if(!this.isLogged){
      this.router.navigateByUrl('/login', {replaceUrl: true})
    }else {
      this.bookService.rentBook(isbn).subscribe(
        data => {
          this.isMyBook.push(isbn);
          this.router.navigate(['/book/', isbn]);
        },
        error => this.createToast(error)
      );
    }
  }

  logout(){
    this.auth.logout().subscribe(
      data => this.router.navigateByUrl('/login', {replaceUrl: true}),
      error => this.createToast(error)
    );
  }


  async createToast(error){
    if(error.status === 0){
      error.error.detail = 'Lost Connection';
    }

    const toast = await this.toastController.create({
      header: 'Error ',
      message: error.error.detail,
      position: 'top',
      duration: 5000,
      buttons:[
        {
          text: 'X',
          role: 'cancel'
        }
      ]
    });
    await toast.present();
  }
}
