import {UserInformation} from './UserInformation';

export class LoggedInUser
{

    private _name :string;

    constructor(theName :string)
    {
        this.name = theName;
    }

    set name(theName :string)
    {
        this._name = theName;
    }

    get name() :string
    {
        return this._name;
    }

    static createLoggedInUserByUserInformation(userInformation :UserInformation) :LoggedInUser
    {
        return new LoggedInUser(userInformation.name);
    }
}