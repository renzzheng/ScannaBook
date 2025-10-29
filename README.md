<img width="2822" height="284" alt="image" src="https://github.com/user-attachments/assets/177f75cf-aef0-4a7b-8e6a-55b711ad3d4b" />
<p align="center">
  <img width="756" height="491" alt="image" src="https://github.com/user-attachments/assets/890d9a09-b070-4f7d-b176-81773864df2b" />
</p>

## Inspiration
Inspired by how cumbersome it can be to sift through thrift store books, or to even catalog your own personal bookshelf, we set out to create `ScannaBook` to aid in this venture.

## What it does
`ScannaBook` takes in an image of a bookshelf and extracts the text from each book spine to get the title and author (if available). It then queries the Google Books API to retrieve the average rating and description for each book so that it can then be presented in a more digestible format on `ScannaBook`'s home page.

## How we built it
For our frontend, we used `Typescript/React` to create the components and the overall layout of our webpage. For the backend, we used `AWS services` and `Pillow` to extract the text, `Google books API` to give us information about each book, `Gemini` to format output to our likings, and then connected all of this to the frontend  using `Flask` to create our fully working application.
<p align="center">
<img width="518" height="623" alt="image" src="https://github.com/user-attachments/assets/eb2d7b17-9bcc-4c83-af63-33914ba30264" />
</p>

## Challenges we ran into
Overcame challenges while learning the AWS Services console, successfully incorporating Rekognition and S3, creating IAM profiles, and integrating these services into our project.
We explored ways to clean up book spine texts for the Google Books API query, cropping individual books to prevent data bleed and removing noise from the text. To efficiently separate titles and authors, we leveraged Gemini AI to structure the data into a clean JSON format, as opposed to simply using regex to clean the texts, making it easier to send to the frontend.

## Accomplishments that we're proud of
We are proud of creating a full-stack webpage that incorporates both frontend and backend functionality. The frontend being the decorative UI and layout of our webpage and the backend being the functionalities that make the frontend components work. This gave us a better idea on what it's like to work on a full-stack development project. We are also proud of our ability to foster teamwork and collaboration under time constraints, efficiently delegating tasks and gaining experience that will benefit future projects.

## What we learned
- Frontend design for transparent, glass-like UI objects.
- Integrating and referencing APIs into our program.
- Implementing AWS services into our backend.
- Processing and cleaning images with Pillow and formatting data with Gemini.
- Connecting backend services to the frontend using Flask.

## What's next for ScannaBook
ScannaBook really excited us when we were in the brainstorming phase of our project as we had many ambitious ideas for UI elements, novel functionalities, and how they would interact with one another in fun, creative, and user-friendly ways. One of our ideas was to add a rotating carousel of book spine images extracted from Rekognition. The book spine images could also be paired with a cover image to create a semi-third dimensional representation of books on our site.


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

---
Ben Cave | Pedro Gomez | Timothy Jeon | Ren-Zhi Zheng
