function [X, Y] = err_k(patches)
	L = 10;
	Y = [];
	d_lin = [];
	for k = 16:2:24
		T = lsh('lsh', L, k, size(patches, 1), patches, 'range', 255);
		avg_lsh_tm = 0.0;
		avg_lin_tm = 0.0;
		err = 0.0; 
		%for j = 1:2
            for i = 100:100:1000
                nnlsh = [];
                while length(nnlsh) < 4
                    [nnlsh, numcand] = lshlookup(patches(:, i), patches, T, 'k', 4, 'distfun', 'lpnorm', 'distargs', {1});
                end
                % Linear search is slow; and we can do it once. 
                if length(d_lin) < 10
                    nnlin = linear_search(patches, i, 4);
                    d_lin(i/100) = norm(patches(:, i)-patches(:, nnlin(2)), 1)+norm(patches(:, i)-patches(:, nnlin(3)), 1)+norm(patches(:, i)-patches(:, nnlin(4)), 1);
                end
                d_lsh = norm(patches(:, i)-patches(:, nnlsh(2)), 1)+norm(patches(:, i)-patches(:, nnlsh(3)), 1)+norm(patches(:, i)-patches(:, nnlsh(4)), 1);
                err = err+1.0*d_lsh/d_lin(i/100);
            end
        %end
		Y = [Y err];
	end
	figure(1); clf; 
	X = 16:2:24;
	plot(X, Y);
end
