
## Inspiration
The biggest inspiration is Google images as we wanted to encapsulate the ability to extract information from pictures/images.
## What it does
Scannabook takes in a image of a bookshelf and extracts the text from the spine of each book to get the title and author (if given) and gives the data to Google books API. This API then uses this information to show the average review and general description for each book.
## How we built it
For our frontend, we used Typescript/React to create the components and the overall layout of our webpage. For the backend, we used AWS services to extract the text, Google books API to give us information about each book, Gemini to format output to our likings, and then connected all this to the frontend to create our fully working application.
## Challenges we ran into
Struggled with implementing AWS services and different apis due to issues with getting keys and unfamiliarity with documentation.
## Accomplishments that we're proud of
We're proud of creating a webpage that incorporates both frontend and backend portions of code. The frontend being the decorative UI and layout of our webpage and the backend being the functionalities that make the frontend components work. This gave us a better idea on what it's like to work on a full stack development project. We're also proud of our ability in fostering teamwork and collaboration under time constrains which gave us the experience needed for future prospects.

## What we learned
Front end design of transparent, glass-like objects. How to reference Google API integrate the data in our program. 
Implementing AWS services such as Rekognition to our backend portion.

## What's next for ScannaBook
ScannaBook really excited us when we were in the brainstorming phase of our project as we had many ambitious ideas for UI elements, novel functionalities, and how they would interact with one another in fun, creative, and user-friendly ways. One of our ideas was to add a rotating carousel of book spine images extracted from Rekognition. The book spine images could also be paired with a cover image to create a semi-third dimensional representation on our site.


---

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
