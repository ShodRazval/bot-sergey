# syntax=docker/dockerfile:1
# FROM python:3.8.10
#
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# RUN pip install --upgrade pip
#
# WORKDIR /application
# COPY . .
#
# RUN pip install -r requirements.txt


# syntax=docker/dockerfile:1
FROM python:3.8.10

WORKDIR bot_seregey-main/
COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

# CMD ["python", "app/main.py"]
#RUN python main.py

# FROM python:3.10.0-bullseye
#
# RUN python3 -m pip install python-telegram
#
# ADD ./*.*

# COPY app/data.py\
#         resources/jokes_parsed.txt\
#         app/main.py\
#         app/prepare_jokes_utils.py\
#         app/requirements.txt\
#         app/tel_bot_utils.py\
#         app/users_count_service.py

# docker build --tag python-docker
# docker tag python-docker:latest python-docker:v1.0.0



# # FROM python:buster
# # RUN pip3 install python-telegram-bot pythonping pyyaml
# # WORKDIR /usr/src/app
# # COPY ./code/. .
# # ENTRYPOINT ["python"]
# # CMD ["main.py"]
#
#
#
# # Specify the Dart SDK base image version using dart:<version> (ex: dart:2.12)
# FROM dart:stable AS build
#
# # Resolve app dependencies.
# WORKDIR /app
# COPY pubspec.* ./
# RUN dart pub get
#
# # Copy app source code and AOT compile it.
# COPY . .
# # Ensure packages are still up-to-date if anything has changed
# RUN dart pub get --offline
#
# # Pay attention to the next line! Write your file name after `bin/`!
# # For example: `RUN dart compile exe bin/your_file_name.dart ...`
# RUN dart compile exe bin/bot_medium.dart -o bin/server
#
# # Build minimal serving image from AOT-compiled `/server` and required system
# # libraries and configuration files stored in `/runtime/` from the build stage.
# FROM scratch
# COPY --from=build /runtime/ /
# COPY --from=build /app/bin/server /app/bin/
#
# # Start server.
# EXPOSE 8080
# CMD ["/app/bin/server"]