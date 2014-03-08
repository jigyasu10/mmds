function [X, Y] = err_l(patches)
	k = 24;
	Y = [];
	d_lin = [];
	for L = 10:2:20
		T = lsh('lsh', L, k, size(patches, 1), patches, 'range', 255);
		avg_lsh_tm = 0.0;
		avg_lin_tm = 0.0;
		err = 0.0; 
		for i = 100:100:1000
			nnlsh = [];
			while length(nnlsh) < 4 % if the thing cycles, we know we need to restart 
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
		Y = [Y err/10];
	end
	figure(1); clf; 
	X = 10:2:20;
	plot(X, Y);
end
