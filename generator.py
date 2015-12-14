def generate_data(n=10, seed=0):
    #n is the amount of peers in network
    #bandwidth is matrix of downloading speed from computer i to computer j
    #data is in mbps
    import numpy as np
    
    if seed:
        np.random.seed(seed)
    
    C = 1.0
    
    pos = np.random.randn(n, 2)
    bandwidth = np.zeros((n, n))
    for i in xrange(n):
        for j in xrange(n):
            if i != j:
                bandwidth[i, j] = C / np.linalg.norm(pos[i] - pos[j]) #* (0.1 + np.random.random_sample())
                
    bound = np.max(bandwidth)
    bandwidth = bandwidth / bound * 0.9
    connection_types = [10.0, 50.0, 100.0]
    upload_speed = np.zeros(n)
    download_speed = np.zeros(n)
    for i in xrange(n):
        speed = connection_types[np.random.randint(0, len(connection_types))]
        bandwidth[:, i] *= speed
        upload_speed[i] = speed
        download_speed[i] = speed
    return np.around(bandwidth, 2), np.around(download_speed, 2), np.around(upload_speed)

def prepare_data(bandwidth, download_speed, upload_speed, file_step, time_step):
    import numpy as np
    file_piece = time_step / file_step
    if np.any(np.amax(bandwidth, axis=0) * file_piece < 1):
        raise Exception("There are peers that has a connection speed slower than accepted; increase the time step")
    if 1 > file_piece * np.min(np.eye(len(download_speed)) * 1e6 + bandwidth):
        print Exception("Timestep is too small: there are connections that can't pass piece within the time step")
        
    return (bandwidth * file_piece).astype(int), \
            (download_speed * file_piece).astype(int), \
            (upload_speed * file_piece).astype(int)