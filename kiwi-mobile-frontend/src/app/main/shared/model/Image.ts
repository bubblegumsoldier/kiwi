export class Image
{
    constructor({id, src, title, type}){
        this.id = id;
        this.src = src;
        this.title = title;
        this.type = type
    }

    public id :string;
    public src :string;
    public title :string;
    public type :string;
    //This. is. ugly.
    public animateDown :boolean;
    public animateUp :boolean;

}

