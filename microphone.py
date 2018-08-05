
def getSound(self):
        # Current chunk of audio data
        data = self.stream.read(self.CHUNK)
        self.frames.append(data)
        wave = self.save(list(self.frames))

        return data
